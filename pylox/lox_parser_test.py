from typing import Generator

import pytest
from lox_error import LoxError
from lox_ast_printer import AstPrinter
from lox_scanner import Scanner
from lox_parser import Parser


@pytest.fixture(autouse=True)
def clear_error() -> Generator[None, None, None]:
    yield
    LoxError.had_error = False


statements: list[tuple[str, list[str], str, bool]] = [
    ("1;", ["(expr 1.0)"], "", False),
    ("1", [], "[line 1] Error at end: Expect ';' after expression.", True),
    ("print 1;", ["(print 1.0)"], "", False),
    (
        "print +*/;\n print 1;",
        ["(print 1.0)"],
        "[line 1] Error at '+': Expect expression.",
        True,
    ),
    (
        "print +*/;\n print 1",
        [],
        "[line 1] Error at '+': Expect expression.\n[line 2] Error at end: Expect ';' after value.",
        True,
    ),
    ("var a = 1; a = 2;", ["(vardecl a 1.0)", "(expr (assign a 2.0))"], "", False),
    (
        "var a = 1; (a) = 2;",
        [],
        "[line 1] Error at '=': Invalid assignment target.",
        True,
    ),
    ("1 + 1 = 2;", [], "[line 1] Error at '=': Invalid assignment target.", True),
]


@pytest.mark.parametrize("source, expected, err_expected, had_error", statements)
def test_parser(
    source: str,
    expected: list[str],
    err_expected: str,
    had_error: bool,
    capfd: pytest.CaptureFixture[str],
) -> None:
    tokens = Scanner(source).scanTokens()
    assert LoxError.had_error is False
    stmts = Parser(tokens).parse()

    out, err = capfd.readouterr()
    print(f"out, err = '{out}', '{err}'")
    assert out.strip() == ""
    assert err.strip() == err_expected
    assert LoxError.had_error is had_error
    if not had_error:
        assert AstPrinter().print(stmts) == expected
