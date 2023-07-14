from typing import Optional

from tests import TestBase
from src.pylox.lox_token import TokenType
from src.pylox.lox_scanner import Scanner


class TestScanner(TestBase):
    def test_null_source(self) -> None:
        tokens = Scanner("").scanTokens()
        self.assertTrue(len(tokens) == 1)
        token = tokens[0]
        self.assertTrue(token.type == TokenType.EOF)
        self.assertTrue(token.lexeme == "")
        self.assertTrue(token.literal is None)
        self.assertTrue(token.line == 1)


    def _test_single_token(self,
        source: str,
        token_type: TokenType,
        literal: Optional[str] = None,
        line: Optional[int] = None,
    ) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        self.assertTrue(len(tokens) == 2 and tokens[1].type == TokenType.EOF)
        token = tokens[0]
        self.assertTrue(token.type == token_type)
        self.assertTrue(token.lexeme == source)
        self.assertTrue(token.literal == literal)
        self.assertTrue(token.line == line)


    def test_single_tokens(self) -> None:
        single_tokens: list[tuple[str, TokenType]] = [
            ("(", TokenType.LEFT_PAREN),
            ("(", TokenType.LEFT_PAREN),
            (")", TokenType.RIGHT_PAREN),
            ("{", TokenType.LEFT_BRACE),
            ("}", TokenType.RIGHT_BRACE),
            (",", TokenType.COMMA),
            (".", TokenType.DOT),
            ("-", TokenType.MINUS),
            ("+", TokenType.PLUS),
            (";", TokenType.SEMICOLON),
            ("*", TokenType.STAR),
        ]

        for token in single_tokens:
            self._test_single_token(token[0], token[1], None, 1)
