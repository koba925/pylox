import sys
from typing import Any
import pytest

from src.pylox.lox_token import TokenType
from src.pylox.lox_scanner import Scanner


def test_null_source() -> None:
    tokens = Scanner("").scanTokens()
    assert len(tokens) == 1
    token = tokens[0]
    assert token.token_type == TokenType.EOF
    assert token.lexeme == ""
    assert token.literal is None
    assert token.line == 1

single_tokens: list[tuple[str, TokenType, Any, int]] = [
    ("(", TokenType.LEFT_PAREN, None, 1),
    (")", TokenType.RIGHT_PAREN, None, 1),
    ("{", TokenType.LEFT_BRACE, None, 1),
    ("}", TokenType.RIGHT_BRACE, None, 1),
    (",", TokenType.COMMA, None, 1),
    (".", TokenType.DOT, None, 1),
    ("-", TokenType.MINUS, None, 1),
    ("+", TokenType.PLUS, None, 1),
    (";", TokenType.SEMICOLON, None, 1),
    ("*", TokenType.STAR, None, 1),
    ("!=", TokenType.BANG_EQUAL, None, 1),
    ("!", TokenType.BANG, None, 1),
    ("==", TokenType.EQUAL_EQUAL, None, 1),
    ("=", TokenType.EQUAL, None, 1),
    ("<=", TokenType.LESS_EQUAL, None, 1),
    ("<", TokenType.LESS, None, 1),
    (">=", TokenType.GREATER_EQUAL, None, 1),
    (">", TokenType.GREATER, None, 1)
]

@pytest.mark.parametrize("source, token_type, literal, line", single_tokens)
def test_single_token(
    source: str,
    token_type: TokenType,
    literal: Any,
    line: int,
) -> None:
    print(source, token_type, literal, line, file=sys.stderr)
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    assert len(tokens) == 2
    assert tokens[1].token_type == TokenType.EOF
    token = tokens[0]
    assert token.token_type == token_type
    assert token.lexeme == source
    assert token.literal == literal
    assert token.line == line
