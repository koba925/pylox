from expr import Visitor, Expr, Binary, Grouping, Literal, Unary
from lox_token import Token, TokenType


class AstPrinter(Visitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping) -> str:
        return self.__parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: Literal) -> str:
        return "nil" if expr.value == None else str(expr.value)

    def visitUnaryExpr(self, expr: Unary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.right)

    def __parenthesize(self, name: str, *exprs: Expr) -> str: 
        s = f"({name}"
        for expr in exprs:
            s += " " + expr.accept(self)
        s += ")"
        return s

if __name__ == "__main__":
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)))

    print(AstPrinter().print(expression))
