from lox_token import Token, TokenType as TT
import lox_expr as EXPR
import lox_stmt as STMT


class AstPrinter(EXPR.Visitor[str], STMT.Visitor[str]):
    def print(self, stmts: list[STMT.Stmt]) -> list[str]:
        return [stmt.accept(self) for stmt in stmts]

    def visit_block_stmt(self, stmt: STMT.Block) -> str:
        return self.__parenthesize("block", *stmt.statements)

    def visit_expression_stmt(self, stmt: STMT.Expression) -> str:
        return self.__parenthesize("expr", stmt.expression)

    def visit_function_stmt(self, stmt: STMT.Function) -> str:
        return self.__parenthesize("function", stmt.name, *stmt.params, *stmt.body)

    def visit_if_stmt(self, stmt: STMT.If) -> str:
        return self.__parenthesize(
            "if", stmt.condition, stmt.then_branch, stmt.else_branch
        )

    def visit_print_stmt(self, stmt: STMT.Print) -> str:
        return self.__parenthesize("print", stmt.expression)

    def visit_return_stmt(self, stmt: STMT.Return) -> str:
        return self.__parenthesize("return", stmt.value)

    def visit_var_stmt(self, stmt: STMT.Var) -> str:
        return self.__parenthesize("vardecl", stmt.name, stmt.initializer)

    def visit_while_stmt(self, stmt: STMT.While) -> str:
        return self.__parenthesize("while", stmt.condition, stmt.body)

    def visit_assign_expr(self, expr: EXPR.Assign) -> str:
        return self.__parenthesize("assign", expr.name, expr.value)

    def visit_binary_expr(self, expr: EXPR.Binary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_call_expr(self, expr: EXPR.Call) -> str:
        return self.__parenthesize("call", expr.callee, *expr.arguments)

    def visit_grouping_expr(self, expr: EXPR.Grouping) -> str:
        return self.__parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: EXPR.Literal) -> str:
        return "nil" if expr.value is None else str(expr.value)

    def visit_logical_expr(self, expr: EXPR.Logical) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_unary_expr(self, expr: EXPR.Unary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr: EXPR.Variable) -> str:
        return expr.name.lexeme

    def __parenthesize(self, name: str, *items: Token | EXPR.Expr | STMT.Stmt | None) -> str:
        s = f"({name}"
        for item in items:
            if isinstance(item, Token):
                s += " " + item.lexeme
            else:
                s += " " + (item.accept(self) if item is not None else "nil")
        s += ")"
        return s


if __name__ == "__main__":
    statements: list[STMT.Stmt] = [
        STMT.Var(Token(TT.IDENTIFIER, "var1", None, 1), None),
        STMT.Expression(EXPR.Assign(Token(TT.IDENTIFIER, "var1", None, 1), EXPR.Literal("aaa"))),
        STMT.Expression(
            EXPR.Call(
                EXPR.Variable(Token(TT.IDENTIFIER, "func_foo", None, 1)),
                Token(TT.RIGHT_PAREN, ")", None, 1),
                [EXPR.Literal("aaa")],
            )
        ),
        STMT.While(EXPR.Literal(True), STMT.Block([STMT.Expression(EXPR.Literal(1)), STMT.Expression(EXPR.Literal(1))])),
        STMT.Function(
            Token(TT.IDENTIFIER, "func1", None, 1),
            [Token(TT.IDENTIFIER, "p1", None, 1), Token(TT.IDENTIFIER, "p2", None, 1)],
            [
                STMT.Print(
                    EXPR.Binary(
                        EXPR.Unary(Token(TT.MINUS, "-", None, 1), EXPR.Literal(123)),
                        Token(TT.STAR, "*", None, 1),
                        EXPR.Grouping(EXPR.Variable(Token(TT.IDENTIFIER, "p1", None, 1))),
                    )
                ),
                STMT.Return(Token(TT.RETURN, "return", None, 1), EXPR.Literal(1)),
            ],
        ),
    ]

    print(*AstPrinter().print(statements), sep="\n")
