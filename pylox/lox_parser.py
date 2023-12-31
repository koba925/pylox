from typing import Optional

from lox_error import LoxError
from lox_token import Token, TokenType as TT
import lox_expr as EXPR
import lox_stmt as STMT


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.__tokens = tokens
        self.__current = 0

    def parse(self) -> list[STMT.Stmt]:
        statements: list[STMT.Stmt] = []
        while not self.__is_at_end():
            statement = self.__declaration()
            if statement is not None:
                statements.append(statement)
        return statements

    def __declaration(self) -> Optional[STMT.Stmt]:
        try:
            if self.__match(TT.FUN):
                return self.__function("function")
            if self.__match(TT.VAR):
                return self.__var_declaration()

            return self.__statement()
        except ParseError:
            self.__syncronize()
            return None

    def __statement(self) -> STMT.Stmt:
        if self.__match(TT.FOR):
            return self.__for_statement()
        if self.__match(TT.IF):
            return self.__if_statement()
        if self.__match(TT.PRINT):
            return self.__print_statement()
        if self.__match(TT.RETURN):
            return self.__return_statement()
        if self.__match(TT.WHILE):
            return self.__while_statement()
        if self.__match(TT.LEFT_BRACE):
            return STMT.Block(self.__block())

        return self.__expression_statement()

    def __for_statement(self) -> STMT.Stmt:
        self.__consume(TT.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer: Optional[STMT.Stmt] = (
            None
            if self.__match(TT.SEMICOLON)
            else self.__var_declaration()
            if self.__match(TT.VAR)
            else self.__expression_statement()
        )

        condition = None if self.__check(TT.SEMICOLON) else self.__expression()
        self.__consume(TT.SEMICOLON, "Expect ';' after loop condition.")

        increment = None if self.__check(TT.RIGHT_PAREN) else self.__expression()
        self.__consume(TT.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.__statement()

        if increment is not None:
            body = STMT.Block([body, STMT.Expression(increment)])

        if condition is None:
            condition = EXPR.Literal(True)
        body = STMT.While(condition, body)

        if initializer is not None:
            body = STMT.Block([initializer, body])

        return body

    def __if_statement(self) -> STMT.Stmt:
        self.__consume(TT.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.__expression()
        self.__consume(TT.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.__statement()
        else_branch = None
        if self.__match(TT.ELSE):
            else_branch = self.__statement()

        return STMT.If(condition, then_branch, else_branch)

    def __print_statement(self) -> STMT.Stmt:
        value = self.__expression()
        self.__consume(TT.SEMICOLON, "Expect ';' after value.")
        return STMT.Print(value)

    def __return_statement(self) -> STMT.Stmt:
        keyword = self.__previous()
        value = None
        if not self.__check(TT.SEMICOLON):
            value = self.__expression()

        self.__consume(TT.SEMICOLON, "Expect ';' after return value.")
        return STMT.Return(keyword, value)

    def __var_declaration(self) -> STMT.Stmt:
        name = self.__consume(TT.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.__match(TT.EQUAL):
            initializer = self.__expression()

        self.__consume(TT.SEMICOLON, "Expect ';' after variable declaration.")
        return STMT.Var(name, initializer)

    def __while_statement(self) -> STMT.Stmt:
        self.__consume(TT.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.__expression()
        self.__consume(TT.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.__statement()

        return STMT.While(condition, body)

    def __expression_statement(self) -> STMT.Stmt:
        expr = self.__expression()
        self.__consume(TT.SEMICOLON, "Expect ';' after expression.")
        return STMT.Expression(expr)

    def __function(self, kind: str) -> STMT.Function:
        name = self.__consume(TT.IDENTIFIER, "Expect " + kind + " name.")
        self.__consume(TT.LEFT_PAREN, "Expect '(' after " + kind + " name.")
        parameters: list[Token] = []
        if not self.__check(TT.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    self.__error(self.__peek(), "Can't have more than 255 prameters.")

                parameters.append(
                    self.__consume(TT.IDENTIFIER, "Expect parameter name.")
                )
                if not self.__match(TT.COMMA):
                    break
        self.__consume(TT.RIGHT_PAREN, "Expect ')' after parameters.")

        self.__consume(TT.LEFT_BRACE, "Expect '{' before " + kind + " body.")
        body = self.__block()
        return STMT.Function(name, parameters, body)

    def __block(self) -> list[STMT.Stmt]:
        statements: list[STMT.Stmt] = []

        while not self.__check(TT.RIGHT_BRACE) and not self.__is_at_end():
            statement = self.__declaration()
            if statement is not None:
                statements.append(statement)

        self.__consume(TT.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def __expression(self) -> EXPR.Expr:
        return self.__assignment()

    def __assignment(self) -> EXPR.Expr:
        expr = self.__or()

        if self.__match(TT.EQUAL):
            equals = self.__previous()
            value = self.__assignment()

            if isinstance(expr, EXPR.Variable):
                name = expr.name
                return EXPR.Assign(name, value)

            self.__error(equals, "Invalid assignment target.")

        return expr

    def __or(self) -> EXPR.Expr:
        expr = self.__and()

        while self.__match(TT.OR):
            operator = self.__previous()
            right = self.__and()
            expr = EXPR.Logical(expr, operator, right)

        return expr

    def __and(self) -> EXPR.Expr:
        expr = self.__equality()

        while self.__match(TT.AND):
            operator = self.__previous()
            right = self.__equality()
            expr = EXPR.Logical(expr, operator, right)

        return expr

    def __equality(self) -> EXPR.Expr:
        expr = self.__comparison()

        while self.__match(TT.BANG_EQUAL, TT.EQUAL_EQUAL):
            operator = self.__previous()
            right = self.__comparison()
            expr = EXPR.Binary(expr, operator, right)

        return expr

    def __comparison(self) -> EXPR.Expr:
        expr = self.__term()

        while self.__match(
            TT.GREATER,
            TT.GREATER_EQUAL,
            TT.LESS,
            TT.LESS_EQUAL,
        ):
            operator = self.__previous()
            right = self.__term()
            expr = EXPR.Binary(expr, operator, right)

        return expr

    def __term(self) -> EXPR.Expr:
        expr = self.__factor()

        while self.__match(TT.MINUS, TT.PLUS):
            operator = self.__previous()
            right = self.__factor()
            expr = EXPR.Binary(expr, operator, right)

        return expr

    def __factor(self) -> EXPR.Expr:
        expr = self.__unary()

        while self.__match(TT.SLASH, TT.STAR):
            operator = self.__previous()
            right = self.__unary()
            expr = EXPR.Binary(expr, operator, right)

        return expr

    def __unary(self) -> EXPR.Expr:
        if self.__match(TT.BANG, TT.MINUS):
            operator = self.__previous()
            right = self.__unary()
            return EXPR.Unary(operator, right)

        return self.__call()

    def __finish_call(self, callee: EXPR.Expr) -> EXPR.Expr:
        arguments: list[EXPR.Expr] = []
        if not self.__check(TT.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    self.__error(self.__peek(), "Can't have more than 255 arguments.")
                arguments.append(self.__expression())
                if not self.__match(TT.COMMA):
                    break

        paren = self.__consume(TT.RIGHT_PAREN, "Expect ')' after arguments")
        return EXPR.Call(callee, paren, arguments)

    def __call(self) -> EXPR.Expr:
        expr = self.__primary()

        while True:
            if self.__match(TT.LEFT_PAREN):
                expr = self.__finish_call(expr)
            else:
                break

        return expr

    def __primary(self) -> EXPR.Expr:
        if self.__match(TT.FALSE):
            return EXPR.Literal(False)
        if self.__match(TT.TRUE):
            return EXPR.Literal(True)
        if self.__match(TT.NIL):
            return EXPR.Literal(None)

        if self.__match(TT.NUMBER, TT.STRING):
            return EXPR.Literal(self.__previous().literal)

        if self.__match(TT.IDENTIFIER):
            return EXPR.Variable(self.__previous())

        if self.__match(TT.LEFT_PAREN):
            expr = self.__expression()
            self.__consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
            return EXPR.Grouping(expr)

        raise self.__error(self.__peek(), "Expect expression.")

    def __match(self, *token_types: TT) -> bool:
        for tt in token_types:
            if self.__check(tt):
                self.__advance()
                return True
        return False

    def __consume(self, token_type: TT, message: str) -> Token:
        if self.__check(token_type):
            return self.__advance()

        raise self.__error(self.__peek(), message)

    def __check(self, token_type: TT) -> bool:
        if self.__is_at_end():
            return False
        return self.__peek().token_type == token_type

    def __advance(self) -> Token:
        if not self.__is_at_end():
            self.__current += 1
        return self.__previous()

    def __is_at_end(self) -> bool:
        return self.__peek().token_type == TT.EOF

    def __peek(self) -> Token:
        return self.__tokens[self.__current]

    def __previous(self) -> Token:
        return self.__tokens[self.__current - 1]

    def __error(self, token: Token, message: str) -> ParseError:
        LoxError.parse_error(token, message)
        return ParseError()

    def __syncronize(self) -> None:
        self.__advance()

        while not self.__is_at_end():
            if self.__previous().token_type == TT.SEMICOLON:
                return
            if self.__peek().token_type in (
                TT.CLASS,
                TT.FUN,
                TT.VAR,
                TT.FOR,
                TT.IF,
                TT.WHILE,
                TT.PRINT,
                TT.RETURN,
            ):
                return

            self.__advance()
