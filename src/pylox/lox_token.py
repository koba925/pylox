from typing import Any
from lox_token_type import TokenType


class Token:
    def __init__(
        self, token_type: TokenType, lexeme: str, literal: Any, line: int
    ) -> None:
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"
