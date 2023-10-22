from typing import Any

from lox_error import LoxError
from lox_token import Token, TokenType as TT


class Scanner:
    __KEYWORDS = {
        "and": TT.AND,
        "class": TT.CLASS,
        "else": TT.ELSE,
        "false": TT.FALSE,
        "for": TT.FOR,
        "fun": TT.FUN,
        "if": TT.IF,
        "nil": TT.NIL,
        "or": TT.OR,
        "print": TT.PRINT,
        "return": TT.RETURN,
        "super": TT.SUPER,
        "this": TT.THIS,
        "true": TT.TRUE,
        "var": TT.VAR,
        "while": TT.WHILE,
    }

    def __init__(self, source: str) -> None:
        self.__source = source
        self.__tokens: list[Token] = []
        self.__start = 0
        self.__current = 0
        self.__line = 1

    def scanTokens(self) -> list[Token]:
        while not self.__is_at_end():
            # We are at the beginning of the next lexeme.
            self.__start = self.__current
            self.__scanToken()

        self.__tokens.append(Token(TT.EOF, "", None, self.__line))
        return self.__tokens

    def __scanToken(self) -> None:
        c = self.__advance()
        if c == "(":
            self.__add_token(TT.LEFT_PAREN)
        elif c == ")":
            self.__add_token(TT.RIGHT_PAREN)
        elif c == "{":
            self.__add_token(TT.LEFT_BRACE)
        elif c == "}":
            self.__add_token(TT.RIGHT_BRACE)
        elif c == ",":
            self.__add_token(TT.COMMA)
        elif c == ".":
            self.__add_token(TT.DOT)
        elif c == "-":
            self.__add_token(TT.MINUS)
        elif c == "+":
            self.__add_token(TT.PLUS)
        elif c == ";":
            self.__add_token(TT.SEMICOLON)
        elif c == "*":
            self.__add_token(TT.STAR)
        elif c == "!":
            self.__add_token(TT.BANG_EQUAL if self.__match("=") else TT.BANG)
        elif c == "=":
            self.__add_token(TT.EQUAL_EQUAL if self.__match("=") else TT.EQUAL)
        elif c == "<":
            self.__add_token(TT.LESS_EQUAL if self.__match("=") else TT.LESS)
        elif c == ">":
            self.__add_token(TT.GREATER_EQUAL if self.__match("=") else TT.GREATER)
        elif c == "/":
            if self.__match("/"):
                # A comment goes until the end of the line.
                while self.__peek() != "\n" and not self.__is_at_end():
                    self.__advance()
            else:
                self.__add_token(TT.SLASH)
        elif c in " \r\t":
            # Ignore whitespaces.
            pass
        elif c == "\n":
            self.__line += 1
        elif c == '"':
            self.__string()
        elif self.__is_digit(c):
            self.__number()
        elif self.__is_alpha(c):
            self.__identifier()
        else:
            LoxError.scan_error(self.__line, "Unexpected character.")

    def __identifier(self) -> None:
        while self.__is_alpha_numeric(self.__peek()):
            self.__advance()

        text = self.__source[self.__start : self.__current]
        self.__add_token(
            self.__KEYWORDS[text] if text in self.__KEYWORDS else TT.IDENTIFIER
        )

    def __number(self) -> None:
        while self.__peek().isdigit():
            self.__advance()

        # Look for a fractional part
        if self.__peek() == "." and self.__peek_next().isdigit():
            # Consume the "."
            self.__advance()

            while self.__peek().isdigit():
                self.__advance()

        self.__add_token(TT.NUMBER, float(self.__source[self.__start : self.__current]))

    def __string(self) -> None:
        while self.__peek() != '"' and not self.__is_at_end():
            if self.__peek() == "\n":
                self.__line += 1
            self.__advance()

        if self.__is_at_end():
            LoxError.scan_error(self.__line, "Unterminated string.")
            return

        # The closing ".
        self.__advance()

        # Trim the surrounding quotes.
        value = self.__source[self.__start + 1 : self.__current - 1]
        self.__add_token(TT.STRING, value)

    def __match(self, expected: str) -> bool:
        if self.__is_at_end():
            return False
        if self.__source[self.__current] != expected:
            return False

        self.__current += 1
        return True

    def __peek(self) -> str:
        return "\0" if self.__is_at_end() else self.__source[self.__current]

    def __peek_next(self) -> str:
        return (
            "\0"
            if self.__current + 1 >= len(self.__source)
            else self.__source[self.__current + 1]
        )

    def __is_digit(self, c: str) -> bool:
        return c.isdigit()

    def __is_alpha(self, c: str) -> bool:
        return c.isalpha() or c == "_"

    def __is_alpha_numeric(self, c: str) -> bool:
        return self.__is_alpha(c) or self.__is_digit(c)

    def __is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    def __advance(self) -> str:
        self.__current += 1
        return self.__source[self.__current - 1]

    def __add_token(self, token_type: TT, literal: Any = None) -> None:
        text = self.__source[self.__start : self.__current]
        self.__tokens.append(Token(token_type, text, literal, self.__line))
