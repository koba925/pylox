from enum import Enum

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
from lox_stmt import (
    Block,
    Stmt,
    StmtVisitor,
    Var,
    Expression,
    Function,
    If,
    Print,
    Return,
    While,
)
from lox_interpreter import Interpreter
from lox_token import Token
from lox_error import LoxError

FunctionType = Enum("FunctionType", ["NONE", "FUNCTION"])


class Resolver(ExprVisitor[None], StmtVisitor[None]):
    def __init__(self, interpreter: Interpreter) -> None:
        self.__interpreter = interpreter
        self.__scopes: list[dict[str, bool]] = []
        self.__currentFunction = FunctionType.NONE

    def __begin_scope(self):
        self.__scopes.append({})

    def __end_scope(self):
        self.__scopes.pop()

    def __declare(self, name: Token):
        if len(self.__scopes) == 0:
            return
        scope = self.__scopes[-1]
        if name.lexeme in scope:
            LoxError.parse_error(
                name, "Already a variable with this name in this scope."
            )
        scope[name.lexeme] = False

    def __define(self, name: Token):
        if len(self.__scopes) == 0:
            return
        self.__scopes[-1][name.lexeme] = True

    def __resolve_local(self, expr: Expr, name: Token):
        for i in reversed(range(len(self.__scopes))):
            if name.lexeme in self.__scopes[i]:
                self.__interpreter.resolve(expr, len(self.__scopes) - 1 - i)
                return

    def __resolve_expression(self, expr: Expr) -> None:
        expr.accept(self)

    def __resolve_statement(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def resolve_statements(self, statements: list[Stmt]) -> None:
        for statement in statements:
            self.__resolve_statement(statement)

    def __resolve_function(self, function: Function, type: FunctionType) -> None:
        enclosingFunction = self.__currentFunction
        self.__currentFunction = type

        self.__begin_scope()
        for param in function.params:
            self.__declare(param)
            self.__define(param)
        self.resolve_statements(function.body)
        self.__end_scope()
        self.__currentFunction = enclosingFunction

    def visit_block_stmt(self, stmt: Block) -> None:
        self.__begin_scope()
        self.resolve_statements(stmt.statements)
        self.__end_scope()

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.__resolve_expression(stmt.expression)

    def visit_function_stmt(self, stmt: Function) -> None:
        self.__declare(stmt.name)
        self.__define(stmt.name)

        self.__resolve_function(stmt, FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt: If) -> None:
        self.__resolve_expression(stmt.condition)
        self.__resolve_statement(stmt.then_branch)
        if stmt.else_branch is not None:
            self.__resolve_statement(stmt.else_branch)

    def visit_print_stmt(self, stmt: Print) -> None:
        self.__resolve_expression(stmt.expression)

    def visit_return_stmt(self, stmt: Return) -> None:
        if self.__currentFunction == FunctionType.NONE:
            LoxError.parse_error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value is not None:
            self.__resolve_expression(stmt.value)

    def visit_var_stmt(self, stmt: Var) -> None:
        self.__declare(stmt.name)
        if stmt.initializer != None:
            self.__resolve_expression(stmt.initializer)
        self.__define(stmt.name)

    def visit_while_stmt(self, stmt: While) -> None:
        self.__resolve_expression(stmt.condition)
        self.__resolve_statement(stmt.body)

    def visit_assign_expr(self, expr: Assign) -> None:
        self.__resolve_expression(expr.value)
        self.__resolve_local(expr, expr.name)

    def visit_binary_expr(self, expr: Binary) -> None:
        self.__resolve_expression(expr.left)
        self.__resolve_expression(expr.right)

    def visit_call_expr(self, expr: Call) -> None:
        self.__resolve_expression(expr.callee)

        for argument in expr.arguments:
            self.__resolve_expression(argument)

    def visit_grouping_expr(self, expr: Grouping) -> None:
        self.__resolve_expression(expr.expression)

    def visit_literal_expr(self, expr: Literal) -> None:
        pass

    def visit_logical_expr(self, expr: Logical) -> None:
        self.__resolve_expression(expr.left)
        self.__resolve_expression(expr.right)

    def visit_variable_expr(self, expr: Variable) -> None:
        if (
            not len(self.__scopes) == 0
            and expr.name.lexeme in self.__scopes[-1]
            and self.__scopes[-1][expr.name.lexeme] == False
        ):
            LoxError.parse_error(
                expr.name, "Can't read local variable in its own initializer."
            )

        self.__resolve_local(expr, expr.name)

    def visit_unary_expr(self, expr: Unary) -> None:
        self.__resolve_expression(expr.right)
