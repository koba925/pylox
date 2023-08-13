from typing import Generator

import pytest

from lox_error import LoxError
from lox_scanner import Scanner
from lox_parser import Parser
from lox_interpreter import Interpreter


@pytest.fixture(autouse=True)
def clear_error() -> Generator[None, None, None]:
    yield
    LoxError.had_error = False
    LoxError.had_runtime_error = False


statements: list[tuple[str, str, str, bool, bool]] = [
    ("print 1;", "1", "", False, False),
    ("print 1.0;", "1", "", False, False),
    ("print 1.1;", "1.1", "", False, False),
    ('print "aaa";', "aaa", "", False, False),
    ("print true;", "true", "", False, False),
    ("print false;", "false", "", False, False),
    ("print nil;", "nil", "", False, False),
    ("print -1;", "-1", "", False, False),
    ("print --1;", "1", "", False, False),
    ("print -true;", "", "Operand must be a number.\n[line 1]", False, True),
    ('print -"aaa";', "", "Operand must be a number.\n[line 1]", False, True),
    ("print !nil;", "true", "", False, False),
    ("print !true;", "false", "", False, False),
    ("print !false;", "true", "", False, False),
    ("print !0;", "false", "", False, False),
    ('print !"";', "false", "", False, False),
    ("print 2+3;", "5", "", False, False),
    ('print "aaa"+"bbb";', "aaabbb", "", False, False),
    (
        'print 2+"aaa";',
        "",
        "Operands must be two numbers or two strings.\n[line 1]",
        False,
        True,
    ),
    (
        'print "aaa"+2;',
        "",
        "Operands must be two numbers or two strings.\n[line 1]",
        False,
        True,
    ),
    ("print 5-3;", "2", "", False, False),
    ("print 5-true;", "", "Operands must be numbers.\n[line 1]", False, True),
    ("print nil-3;", "", "Operands must be numbers.\n[line 1]", False, True),
    ("print 2*3;", "6", "", False, False),
    ("print nil*3;", "", "Operands must be numbers.\n[line 1]", False, True),
    ("print 4/2;", "2", "", False, False),
    ("print 4/nil;", "", "Operands must be numbers.\n[line 1]", False, True),
    ("print 2>1;", "true", "", False, False),
    ("print 1>2;", "false", "", False, False),
    ("print 1>1;", "false", "", False, False),
    ("print 1>nil;", "", "Operands must be numbers.\n[line 1]", False, True),
    ("print 2>=1;", "true", "", False, False),
    ("print 1>=2;", "false", "", False, False),
    ("print 1>=1;", "true", "", False, False),
    ("print 1>=nil;", "", "Operands must be numbers.\n[line 1]", False, True),
    ("print 1<2;", "true", "", False, False),
    ("print 2<1;", "false", "", False, False),
    ("print 1<1;", "false", "", False, False),
    ("print 1<nil;", "", "Operands must be numbers.\n[line 1]", False, True),
    ("print 1<=2;", "true", "", False, False),
    ("print 2<=1;", "false", "", False, False),
    ("print 1<=1;", "true", "", False, False),
    ("print 1<=nil;", "", "Operands must be numbers.\n[line 1]", False, True),
    ("print 1==1;", "true", "", False, False),
    ("print 2==1;", "false", "", False, False),
    ('print "aaa"=="aaa";', "true", "", False, False),
    ('print "aaa"=="aab";', "false", "", False, False),
    ("print true==true;", "true", "", False, False),
    ("print false==false;", "true", "", False, False),
    ("print true==false;", "false", "", False, False),
    ('print 1=="aaa";', "false", "", False, False),
    ("print 1==true;", "false", "", False, False),
    ("print 0==false;", "false", "", False, False),
    ("print 1==nil;", "false", "", False, False),
    ("print 1!=1;", "false", "", False, False),
    ("print 2!=1;", "true", "", False, False),
    ('print "aaa"!="aaa";', "false", "", False, False),
    ('print "aaa"!="aab";', "true", "", False, False),
    ("print true!=true;", "false", "", False, False),
    ("print false!=false;", "false", "", False, False),
    ("print true!=false;", "true", "", False, False),
    ('print 1!="aaa";', "true", "", False, False),
    ("print 1!=true;", "true", "", False, False),
    ("print 0!=false;", "true", "", False, False),
    ("print 1!=nil;", "true", "", False, False),
    ("print (2+3)*4;", "20", "", False, False),
]


@pytest.mark.parametrize(
    "source, out_expected, err_expected, had_error, had_runtime_error", statements
)
def test_statements(
    source: str,
    out_expected: str,
    err_expected: str,
    had_error: bool,
    had_runtime_error: bool,
    capfd: pytest.CaptureFixture[str],
) -> None:
    tokens = Scanner(source).scanTokens()
    assert LoxError.had_error is False
    stmts = Parser(tokens).parse()
    assert LoxError.had_error is False
    assert stmts is not None
    Interpreter().interpret(stmts)

    out, err = capfd.readouterr()
    print(f"out, err = '{out}', '{err}'")
    assert out.strip() == out_expected
    assert err.strip() == err_expected
    assert LoxError.had_error is had_error
    assert LoxError.had_runtime_error is had_runtime_error
