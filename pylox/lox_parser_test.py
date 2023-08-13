from typing import Generator

import pytest

from lox_error import LoxError
from lox_scanner import Scanner
from lox_parser import Parser
from lox_ast_printer import AstPrinter


@pytest.fixture(autouse=True)
def clear_error() -> Generator[None, None, None]:
    yield
    LoxError.had_error = False


statements: list[tuple[str, list[str], bool]] = [
    ("1;", ["(expr 1.0)"], False),
    ("print 1;", ["(print 1.0)"], False),
]


@pytest.mark.parametrize("source, expected, had_error", statements)
def test_parser(
    source: str,
    expected: list[str],
    had_error: bool,
) -> None:
    tokens = Scanner(source).scanTokens()
    assert LoxError.had_error is False
    stmts = Parser(tokens).parse()

    assert AstPrinter().print(stmts) == expected
    assert LoxError.had_error is had_error
