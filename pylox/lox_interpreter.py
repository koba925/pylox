from typing import Any

from lox_environment import Environment
from lox_error import LoxError
from lox_expr import (
    Assign,
    Binary,
    Call,
    Expr,
    ExprVisitor,
    Grouping,
    Literal,
    Logical,
    Unary,
    Variable,
)
from lox_runtime_error import LoxRuntimeError
from lox_stmt import (
    Block,
    Expression,
    Function,
    If,
    Print,
    Return,
    Stmt,
    StmtVisitor,
    Var,
    While,
)
from lox_token import Token
from lox_token import TokenType as TT
from lox_callable import LoxCallable, Clock
from lox_function import LoxFunction
from lox_return import ReturnException

# TODO: use operator module


class Interpreter(ExprVisitor[Any], StmtVisitor[None]):
    def __init__(self) -> None:
        self.__globals = Environment()
        self.__environment = self.__globals
        self.__locals: dict[Expr, int] = {}

        self.__globals.define("clock", Clock())

    def interpret(self, statements: list[Stmt]) -> None:
        try:
            for statement in statements:
                self.__execute(statement)
        except LoxRuntimeError as e:
            LoxError.runtime_error(e)

    def __evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def __execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def resolve(self, expr: Expr, depth: int) -> None:
        self.__locals[expr] = depth

    def execute_block(self, statements: list[Stmt], environment: Environment) -> None:
        previous = self.__environment

        try:
            self.__environment = environment

            for statement in statements:
                self.__execute(statement)
        finally:
            self.__environment = previous

    def visit_block_stmt(self, stmt: Block) -> None:
        self.execute_block(stmt.statements, Environment(self.__environment))

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.__evaluate(stmt.expression)

    def visit_function_stmt(self, stmt: "Function") -> None:
        function = LoxFunction(stmt, self.__environment)
        self.__environment.define(stmt.name.lexeme, function)

    def visit_if_stmt(self, stmt: If) -> None:
        if self.__is_truthy(self.__evaluate(stmt.condition)):
            self.__execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.__execute(stmt.else_branch)

    def visit_print_stmt(self, stmt: Print) -> None:
        value = self.__evaluate(stmt.expression)
        print(self.__stringify(value))

    def visit_return_stmt(self, stmt: Return) -> None:
        value = None
        if stmt.value is not None:
            value = self.__evaluate(stmt.value)

        raise ReturnException(value)

    def visit_var_stmt(self, stmt: Var) -> None:
        value = None
        if stmt.initializer is not None:
            value = self.__evaluate(stmt.initializer)

        self.__environment.define(stmt.name.lexeme, value)

    def visit_while_stmt(self, stmt: While) -> None:
        while self.__is_truthy(self.__evaluate(stmt.condition)):
            self.__execute(stmt.body)

    def visit_assign_expr(self, expr: Assign) -> Any:
        value = self.__evaluate(expr.value)
        if expr in self.__locals:
            distance = self.__locals[expr]
            self.__environment.assign_at(distance, expr.name, value)
        else:
            self.__globals.assign(expr.name, value)
        return value

    def visit_binary_expr(self, expr: Binary) -> Any:
        left = self.__evaluate(expr.left)
        right = self.__evaluate(expr.right)

        if expr.operator.token_type == TT.BANG_EQUAL:
            return not self.__is_equal(left, right)
        if expr.operator.token_type == TT.EQUAL_EQUAL:
            return self.__is_equal(left, right)

        if expr.operator.token_type == TT.GREATER:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        if expr.operator.token_type == TT.GREATER_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        if expr.operator.token_type == TT.LESS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        if expr.operator.token_type == TT.LESS_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)

        if expr.operator.token_type == TT.MINUS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        if expr.operator.token_type == TT.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise LoxRuntimeError(
                expr.operator, "Operands must be two numbers or two strings."
            )
        if expr.operator.token_type == TT.SLASH:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        if expr.operator.token_type == TT.STAR:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) * float(right)

        # Unreachable.
        return None

    def visit_call_expr(self, expr: Call) -> Any:
        callee = self.__evaluate(expr.callee)

        arguments: list[Any] = []
        for argument in expr.arguments:
            arguments.append(self.__evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

        if len(arguments) != callee.arity():
            raise LoxRuntimeError(
                expr.paren,
                f"Expected {callee.arity()} arguments but got {len(arguments)}.",
            )

        return callee.call(self, arguments)

    def visit_grouping_expr(self, expr: Grouping) -> Any:
        return self.__evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal) -> Any:
        return expr.value

    def visit_logical_expr(self, expr: Logical) -> Any:
        left = self.__evaluate(expr.left)

        if expr.operator.token_type == TT.OR:
            if self.__is_truthy(left):
                return left
        else:
            if not self.__is_truthy(left):
                return left

        return self.__evaluate(expr.right)

    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.__evaluate(expr.right)

        if expr.operator.token_type == TT.BANG:
            return not self.__is_truthy(right)
        if expr.operator.token_type == TT.MINUS:
            self.__check_number_operand(expr.operator, right)
            return -float(right)

        # Unreachable.
        return None

    def visit_variable_expr(self, expr: Variable) -> Any:
        return self.__lookup_variable(expr.name, expr)

    def __lookup_variable(self, name: Token, expr: Expr) -> Any:
        if expr in self.__locals:
            return self.__environment.get_at(self.__locals[expr], name.lexeme)
        else:
            return self.__globals.get(name)

    def __check_number_operand(self, operator: Token, operand: Any) -> None:
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def __check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")

    def __is_truthy(self, obj: Any) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def __is_equal(self, a: Any, b: Any) -> bool:
        # pylint: disable=unidiomatic-typecheck # cannot check by isinstance
        return type(a) == type(b) and a == b

    def __stringify(self, obj: Any) -> str:
        if obj is None:
            return "nil"
        if isinstance(obj, bool):
            return "true" if obj is True else "false"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)
