import sys
from typing import Any, Generator
import pytest

from lox_error import LoxError
from lox_token import TokenType
from lox_scanner import Scanner


@pytest.fixture(autouse=True)
def clear_error() -> Generator[None, None, None]:
    yield
    LoxError.had_error = False


def test_null_source() -> None:
    tokens = Scanner("").scanTokens()
    assert LoxError.had_error == False
    assert len(tokens) == 1
    token = tokens[0]
    assert token.token_type == TokenType.EOF
    assert token.lexeme == ""
    assert token.literal is None
    assert token.line == 1


def test_unexpected_character() -> None:
    tokens = Scanner(":").scanTokens()
    assert LoxError.had_error == True


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
    (">", TokenType.GREATER, None, 1),
    ("/", TokenType.SLASH, None, 1),
    ('"abc"', TokenType.STRING, "abc", 1),
    ('"ab\nc"', TokenType.STRING, "ab\nc", 2),
    ("1", TokenType.NUMBER, 1, 1),
    ("123", TokenType.NUMBER, 123, 1),
    ("1.0", TokenType.NUMBER, 1.0, 1),
    ("a", TokenType.IDENTIFIER, None, 1),
    ("_", TokenType.IDENTIFIER, None, 1),
    ("_a", TokenType.IDENTIFIER, None, 1),
    ("and", TokenType.AND, None, 1),
    ("class", TokenType.CLASS, None, 1),
    ("else", TokenType.ELSE, None, 1),
    ("false", TokenType.FALSE, None, 1),
    ("for", TokenType.FOR, None, 1),
    ("fun", TokenType.FUN, None, 1),
    ("if", TokenType.IF, None, 1),
    ("nil", TokenType.NIL, None, 1),
    ("or", TokenType.OR, None, 1),
    ("print", TokenType.PRINT, None, 1),
    ("return", TokenType.RETURN, None, 1),
    ("super", TokenType.SUPER, None, 1),
    ("this", TokenType.THIS, None, 1),
    ("true", TokenType.TRUE, None, 1),
    ("var", TokenType.VAR, None, 1),
    ("while", TokenType.WHILE, None, 1)
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
    assert LoxError.had_error == False
    tokens = scanner.scanTokens()
    assert len(tokens) == 2
    assert tokens[1].token_type == TokenType.EOF
    token = tokens[0]
    assert token.token_type == token_type
    assert token.lexeme == source
    assert token.literal == literal
    assert token.line == line


def test_comment_to_end() -> None:
    tokens = Scanner("+//").scanTokens()
    assert LoxError.had_error == False
    assert len(tokens) == 2
    assert tokens[0].token_type == TokenType.PLUS
    assert tokens[1].token_type == TokenType.EOF


def test_comment_to_newline() -> None:
    tokens = Scanner("+// aaa\n-").scanTokens()
    assert LoxError.had_error == False
    assert len(tokens) == 3
    assert tokens[0].token_type == TokenType.PLUS
    assert tokens[1].token_type == TokenType.MINUS
    assert tokens[2].token_type == TokenType.EOF
    assert LoxError.had_error == False


def test_whitespaces() -> None:
    tokens = Scanner("+ -\r;\t,\n.").scanTokens()
    assert LoxError.had_error == False
    assert len(tokens) == 6
    assert tokens[0].token_type == TokenType.PLUS
    assert tokens[1].token_type == TokenType.MINUS
    assert tokens[2].token_type == TokenType.SEMICOLON
    assert tokens[3].token_type == TokenType.COMMA
    assert tokens[3].line == 1
    assert tokens[4].token_type == TokenType.DOT
    assert tokens[4].line == 2
    assert tokens[5].token_type == TokenType.EOF


def test_unterminated_string() -> None:
    tokens = Scanner('"abc').scanTokens()
    assert LoxError.had_error == True

def test_number_leading_dot() -> None:
    tokens = Scanner('.123').scanTokens()
    assert LoxError.had_error == False
    assert len(tokens) == 3
    assert tokens[0].token_type == TokenType.DOT
    assert tokens[1].token_type == TokenType.NUMBER
    assert tokens[2].token_type == TokenType.EOF

def test_number_trailing_dot() -> None:
    tokens = Scanner('123.').scanTokens()
    assert LoxError.had_error == False
    assert len(tokens) == 3
    assert tokens[0].token_type == TokenType.NUMBER
    assert tokens[1].token_type == TokenType.DOT
    assert tokens[2].token_type == TokenType.EOF
