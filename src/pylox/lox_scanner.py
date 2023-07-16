from typing import Any

from lox_error import LoxError
from lox_token import TokenType, Token


class Scanner:
    def __init__(self, source: str) -> None:
        self.__source = source
        self.__tokens: list[Token] = []
        self.__start = 0
        self.__current = 0
        self.__line = 1

    def scanTokens(self) -> list[Token]:
        while not self.__isAtEnd():
            # We are at the beginning of the next lexeme.
            self.__start = self.__current
            self.__scanToken()

        self.__tokens.append(Token(TokenType.EOF, "", None, self.__line))
        return self.__tokens

    def __scanToken(self) -> None:
        c = self.__advance()
        if c == "(":
            self.__addToken(TokenType.LEFT_PAREN)
        elif c == ")":
            self.__addToken(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.__addToken(TokenType.LEFT_BRACE)
        elif c == "}":
            self.__addToken(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.__addToken(TokenType.COMMA)
        elif c == ".":
            self.__addToken(TokenType.DOT)
        elif c == "-":
            self.__addToken(TokenType.MINUS)
        elif c == "+":
            self.__addToken(TokenType.PLUS)
        elif c == ";":
            self.__addToken(TokenType.SEMICOLON)
        elif c == "*":
            self.__addToken(TokenType.STAR)
        elif c == "!":
            self.__addToken(
                TokenType.BANG_EQUAL if self.__match("=") else TokenType.BANG
            )
        elif c == "=":
            self.__addToken(
                TokenType.EQUAL_EQUAL if self.__match("=") else TokenType.EQUAL
            )
        elif c == "<":
            self.__addToken(
                TokenType.LESS_EQUAL if self.__match("=") else TokenType.LESS
            )
        elif c == ">":
            self.__addToken(
                TokenType.GREATER_EQUAL if self.__match("=") else TokenType.GREATER
            )
        elif c == "/":
            if self.__match("/"):
                # A comment goes until the end of the line.
                while self.__peek() != "\n" and not self.__isAtEnd():
                    self.__advance()
            else:
                self.__addToken(TokenType.SLASH)
        elif c in " \r\t":
            # Ignore whitespaces.
            pass
        elif c == "\n":
            self.__line += 1
        elif c == '"':
            self.__string()
        else:
            LoxError.error(self.__line, "Unexpected character.")

    def __string(self) -> None:
        while self.__peek() != "\"" and not self.__isAtEnd():
            if self.__peek() == "\n":
                self.__line += 1
            self.__advance()
        
        if self.__isAtEnd():
            LoxError.error(self.__line, "Unterminated string.")
            return
        
        # The closing ".
        self.__advance()

        # Trim the surrounding quotes.
        value = self.__source[self.__start+1:self.__current-1]
        self.__addToken(TokenType.STRING, value)

    def __match(self, expected: str) -> bool:
        if self.__isAtEnd():
            return False
        if self.__source[self.__current] != expected:
            return False

        self.__current += 1
        return True

    def __peek(self) -> str:
        return "\0" if self.__isAtEnd() else self.__source[self.__current]

    def __isAtEnd(self) -> bool:
        return self.__current >= len(self.__source)

    def __advance(self) -> str:
        self.__current += 1
        return self.__source[self.__current - 1]

    def __addToken(self, token_type: TokenType, literal: Any = None) -> None:
        text = self.__source[self.__start : self.__current]
        self.__tokens.append(Token(token_type, text, literal, self.__line))
