from lox_expr import (
    Assign,
    Binary,
    Expr,
    ExprVisitor,
    Grouping,
    Literal,
    Logical,
    Unary,
    Variable,
)
from lox_stmt import Block, Expression, Print, If, Stmt, StmtVisitor, Var
from lox_token import Token
from lox_token import TokenType as TT


class AstPrinter(ExprVisitor[str], StmtVisitor[str]):
    def print(self, stmts: list[Stmt]) -> list[str]:
        return [stmt.accept(self) for stmt in stmts if stmt is not None]

    def visit_block_stmt(self, stmt: Block) -> str:
        return self.__parenthesize("block", *stmt.statements)

    def visit_expression_stmt(self, stmt: Expression) -> str:
        return self.__parenthesize("expr", stmt.expression)

    def visit_if_stmt(self, stmt: If) -> str:
        return self.__parenthesize(
            "if", stmt.condition, stmt.then_branch, stmt.else_branch
        )

    def visit_print_stmt(self, stmt: Print) -> str:
        return self.__parenthesize("print", stmt.expression)

    def visit_var_stmt(self, stmt: Var) -> str:
        return self.__parenthesize("vardecl", stmt.name, stmt.initializer)

    def visit_assign_expr(self, expr: Assign) -> str:
        return self.__parenthesize("assign", expr.name, expr.value)

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.__parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        return "nil" if expr.value is None else str(expr.value)

    def visit_logical_expr(self, expr: Logical) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr: Variable) -> str:
        return expr.name.lexeme

    def __parenthesize(self, name: str, *items: Token | Expr | Stmt | None) -> str:
        s = f"({name}"
        for item in items:
            if isinstance(item, Token):
                s += " " + item.lexeme
            else:
                s += " " + (item.accept(self) if item is not None else "nil")
        s += ")"
        return s


if __name__ == "__main__":
    statements: list[Stmt] = [
        Var(Token(TT.IDENTIFIER, "var1", None, 1), None),
        Assign(Token(TT.IDENTIFIER, "var1", None, 1), Literal("aaa")),
        Print(
            Binary(
                Unary(Token(TT.MINUS, "-", None, 1), Literal(123)),
                Token(TT.STAR, "*", None, 1),
                Grouping(Variable(Token(TT.IDENTIFIER, "var1", None, 1))),
            )
        ),
        Block([Expression(Literal(1)), Expression(Literal(1))]),
    ]

    print(*AstPrinter().print(statements), sep="\n")
