from lox_expr import ExprVisitor, Expr, Binary, Grouping, Literal, Unary
from lox_stmt import StmtVisitor, Stmt, Expression, Print
from lox_token import Token, TokenType


class AstPrinter(ExprVisitor[str], StmtVisitor[str]):
    def print(self, stmts: list[Stmt]) -> list[str]:
        return [stmt.accept(self) for stmt in stmts]

    def visitExpressionStmt(self, stmt: Expression) -> str:
        return self.__parenthesize("expr", stmt.expression)

    def visitPrintStmt(self, stmt: Print) -> str:
        return self.__parenthesize("print", stmt.expression)

    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping) -> str:
        return self.__parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: Literal) -> str:
        return "nil" if expr.value is None else str(expr.value)

    def visitUnaryExpr(self, expr: Unary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.right)

    def __parenthesize(self, name: str, *exprs: Expr | Stmt) -> str:
        s = f"({name}"
        for expr in exprs:
            s += " " + expr.accept(self)
        s += ")"
        return s


if __name__ == "__main__":
    statements = [
        Print(
            Binary(
                Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
                Token(TokenType.STAR, "*", None, 1),
                Grouping(Literal(45.67)),
            )
        ),
        Expression(Literal(1)),
    ]

    print(*AstPrinter().print(statements), sep="\n")
