import sys
from typing import Optional

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


def __test_single_token(
    source: str,
    token_type: TokenType,
    literal: Optional[str] = None,
    line: Optional[int] = None,
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


def test_single_tokens() -> None:
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
        ("!=", TokenType.BANG_EQUAL),
        ("!", TokenType.BANG),
        ("==", TokenType.EQUAL_EQUAL),
        ("=", TokenType.EQUAL),
        ("<=", TokenType.LESS_EQUAL),
        ("<", TokenType.LESS),
        (">=", TokenType.GREATER_EQUAL),
        (">", TokenType.GREATER)
    ]

    for token in single_tokens:
        __test_single_token(token[0], token[1], None, 1)
