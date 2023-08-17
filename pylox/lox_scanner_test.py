import sys
from typing import Any, Generator

import pytest
from lox_error import LoxError
from lox_scanner import Scanner
from lox_token import TokenType as TT


@pytest.fixture(autouse=True)
def clear_error() -> Generator[None, None, None]:
    yield
    LoxError.had_error = False


def test_null_source() -> None:
    tokens = Scanner("").scanTokens()
    assert LoxError.had_error is False
    assert len(tokens) == 1
    token = tokens[0]
    assert token.token_type == TT.EOF
    assert token.lexeme == ""
    assert token.literal is None
    assert token.line == 1


def test_unexpected_character() -> None:
    Scanner(":").scanTokens()
    assert LoxError.had_error is True


single_tokens: list[tuple[str, TT, Any, int]] = [
    ("(", TT.LEFT_PAREN, None, 1),
    (")", TT.RIGHT_PAREN, None, 1),
    ("{", TT.LEFT_BRACE, None, 1),
    ("}", TT.RIGHT_BRACE, None, 1),
    (",", TT.COMMA, None, 1),
    (".", TT.DOT, None, 1),
    ("-", TT.MINUS, None, 1),
    ("+", TT.PLUS, None, 1),
    (";", TT.SEMICOLON, None, 1),
    ("*", TT.STAR, None, 1),
    ("!=", TT.BANG_EQUAL, None, 1),
    ("!", TT.BANG, None, 1),
    ("==", TT.EQUAL_EQUAL, None, 1),
    ("=", TT.EQUAL, None, 1),
    ("<=", TT.LESS_EQUAL, None, 1),
    ("<", TT.LESS, None, 1),
    (">=", TT.GREATER_EQUAL, None, 1),
    (">", TT.GREATER, None, 1),
    ("/", TT.SLASH, None, 1),
    ('"abc"', TT.STRING, "abc", 1),
    ('"ab\nc"', TT.STRING, "ab\nc", 2),
    ("1", TT.NUMBER, 1, 1),
    ("123", TT.NUMBER, 123, 1),
    ("1.0", TT.NUMBER, 1.0, 1),
    ("a", TT.IDENTIFIER, None, 1),
    ("_", TT.IDENTIFIER, None, 1),
    ("_a", TT.IDENTIFIER, None, 1),
    ("and", TT.AND, None, 1),
    ("class", TT.CLASS, None, 1),
    ("else", TT.ELSE, None, 1),
    ("false", TT.FALSE, None, 1),
    ("for", TT.FOR, None, 1),
    ("fun", TT.FUN, None, 1),
    ("if", TT.IF, None, 1),
    ("nil", TT.NIL, None, 1),
    ("or", TT.OR, None, 1),
    ("print", TT.PRINT, None, 1),
    ("return", TT.RETURN, None, 1),
    ("super", TT.SUPER, None, 1),
    ("this", TT.THIS, None, 1),
    ("true", TT.TRUE, None, 1),
    ("var", TT.VAR, None, 1),
    ("while", TT.WHILE, None, 1),
]


@pytest.mark.parametrize("source, token_type, literal, line", single_tokens)
def test_single_token(
    source: str,
    token_type: TT,
    literal: Any,
    line: int,
) -> None:
    print(source, token_type, literal, line, file=sys.stderr)
    scanner = Scanner(source)
    assert LoxError.had_error is False
    tokens = scanner.scanTokens()
    assert len(tokens) == 2
    assert tokens[1].token_type == TT.EOF
    token = tokens[0]
    assert token.token_type == token_type
    assert token.lexeme == source
    assert token.literal == literal
    assert token.line == line


def test_comment_to_end() -> None:
    tokens = Scanner("+//").scanTokens()
    assert LoxError.had_error is False
    assert len(tokens) == 2
    assert tokens[0].token_type == TT.PLUS
    assert tokens[1].token_type == TT.EOF


def test_comment_to_newline() -> None:
    tokens = Scanner("+// aaa\n-").scanTokens()
    assert LoxError.had_error is False
    assert len(tokens) == 3
    assert tokens[0].token_type == TT.PLUS
    assert tokens[1].token_type == TT.MINUS
    assert tokens[2].token_type == TT.EOF


def test_whitespaces() -> None:
    tokens = Scanner("+ -\r;\t,\n.").scanTokens()
    assert LoxError.had_error is False
    assert len(tokens) == 6
    assert tokens[0].token_type == TT.PLUS
    assert tokens[1].token_type == TT.MINUS
    assert tokens[2].token_type == TT.SEMICOLON
    assert tokens[3].token_type == TT.COMMA
    assert tokens[3].line == 1
    assert tokens[4].token_type == TT.DOT
    assert tokens[4].line == 2
    assert tokens[5].token_type == TT.EOF


def test_unterminated_string() -> None:
    Scanner('"abc').scanTokens()
    assert LoxError.had_error is True


def test_number_leading_dot() -> None:
    tokens = Scanner(".123").scanTokens()
    assert LoxError.had_error is False
    assert len(tokens) == 3
    assert tokens[0].token_type == TT.DOT
    assert tokens[1].token_type == TT.NUMBER
    assert tokens[2].token_type == TT.EOF


def test_number_trailing_dot() -> None:
    tokens = Scanner("123.").scanTokens()
    assert LoxError.had_error is False
    assert len(tokens) == 3
    assert tokens[0].token_type == TT.NUMBER
    assert tokens[1].token_type == TT.DOT
    assert tokens[2].token_type == TT.EOF
