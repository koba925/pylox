from typing import Any

from lox_expr import Binary, Expr, Grouping, Literal, Visitor, Unary
from lox_token import Token, TokenType
from lox_error import LoxError
from lox_runtime_error import LoxRuntimeError

# TODO: use operator module


class Interpreter(Visitor[Any]):
    def interpret(self, expression: Expr) -> None:
        try:
            value = self.__evaluate(expression)
            print(self.__stringify(value))
        except LoxRuntimeError as e:
            LoxError.runtime_error(e)

    def __evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary) -> Any:
        left = self.__evaluate(expr.left)
        right = self.__evaluate(expr.right)

        if expr.operator.token_type == TokenType.BANG_EQUAL:
            return not self.__is_equal(left, right)
        if expr.operator.token_type == TokenType.EQUAL_EQUAL:
            return self.__is_equal(left, right)

        if expr.operator.token_type == TokenType.GREATER:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        if expr.operator.token_type == TokenType.GREATER_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        if expr.operator.token_type == TokenType.LESS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        if expr.operator.token_type == TokenType.LESS_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)

        if expr.operator.token_type == TokenType.MINUS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        if expr.operator.token_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise LoxRuntimeError(
                expr.operator, "Operands must be two numbers or two strings."
            )
        if expr.operator.token_type == TokenType.SLASH:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        if expr.operator.token_type == TokenType.STAR:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) * float(right)

        # Unreachable.
        return None

    def visitGroupingExpr(self, expr: Grouping) -> Any:
        return self.__evaluate(expr.expression)

    def visitLiteralExpr(self, expr: Literal) -> Any:
        return expr.value

    def visitUnaryExpr(self, expr: Unary) -> Any:
        right = self.__evaluate(expr.right)

        if expr.operator.token_type == TokenType.BANG:
            return not self.__is_truthy(right)
        if expr.operator.token_type == TokenType.MINUS:
            self.__check_number_operand(expr.operator, right)
            return -float(right)

        # Unreachable.
        return None

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
        return type(a) == type(b) and a == b  # pylint: disable=C0123 # cannot check by isinstance

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
