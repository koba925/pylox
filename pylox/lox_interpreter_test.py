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


expressions: list[tuple[str, str, str, bool, bool]] = [
    ("1", "1", "", False, False),
    ("1.0", "1", "", False, False),
    ("1.1", "1.1", "", False, False),
    ("\"aaa\"", "aaa", "", False, False),
    ("true", "true", "", False, False),
    ("false", "false", "", False, False),
    ("nil", "nil", "", False, False),
    ("-1", "-1", "", False, False),
    ("--1", "1", "", False, False),
    ("-true", "", "Operand must be a number.\n[line 1]", False, True),
    ("-\"aaa\"", "", "Operand must be a number.\n[line 1]", False, True),
    ("!nil", "true", "", False, False),
    ("!true", "false", "", False, False),
    ("!false", "true", "", False, False),
    ("!0", "false", "", False, False),
    ("!\"\"", "false", "", False, False),
    ("2+3", "5", "", False, False),
    ("\"aaa\"+\"bbb\"", "aaabbb", "", False, False),
    ("2+\"aaa\"", "", "Operands must be two numbers or two strings.\n[line 1]", False, True),
    ("\"aaa\"+2", "", "Operands must be two numbers or two strings.\n[line 1]", False, True),
    ("5-3", "2", "", False, False),
    ("5-true", "", "Operands must be numbers.\n[line 1]", False, True),
    ("nil-3", "", "Operands must be numbers.\n[line 1]", False, True),
    ("2*3", "6", "", False, False),
    ("nil*3", "", "Operands must be numbers.\n[line 1]", False, True),
    ("4/2", "2", "", False, False),
    ("4/nil", "", "Operands must be numbers.\n[line 1]", False, True),
    ("2>1", "true", "", False, False),
    ("1>2", "false", "", False, False),
    ("1>1", "false", "", False, False),
    ("1>nil", "", "Operands must be numbers.\n[line 1]", False, True),
    ("2>=1", "true", "", False, False),
    ("1>=2", "false", "", False, False),
    ("1>=1", "true", "", False, False),
    ("1>=nil", "", "Operands must be numbers.\n[line 1]", False, True),
    ("1<2", "true", "", False, False),
    ("2<1", "false", "", False, False),
    ("1<1", "false", "", False, False),
    ("1<nil", "", "Operands must be numbers.\n[line 1]", False, True),
    ("1<=2", "true", "", False, False),
    ("2<=1", "false", "", False, False),
    ("1<=1", "true", "", False, False),
    ("1<=nil", "", "Operands must be numbers.\n[line 1]", False, True),
    ("1==1", "true", "", False, False),
    ("2==1", "false", "", False, False),
    ("\"aaa\"==\"aaa\"", "true", "", False, False),
    ("\"aaa\"==\"aab\"", "false", "", False, False),
    ("true==true", "true", "", False, False),
    ("false==false", "true", "", False, False),
    ("true==false", "false", "", False, False),
    ("1==\"aaa\"", "false", "", False, False),
    ("1==true", "false", "", False, False), # Python evaluates this to True
    ("0==false", "false", "", False, False), # Python evaluates this to True
    ("1==nil", "false", "", False, False) ,
    ("1!=1", "false", "", False, False) ,
    ("2!=1", "true", "", False, False) ,
    ("\"aaa\"!=\"aaa\"", "false", "", False, False) ,
    ("\"aaa\"!=\"aab\"", "true", "", False, False) ,
    ("true!=true", "false", "", False, False) ,
    ("false!=false", "false", "", False, False) ,
    ("true!=false", "true", "", False, False) ,
    ("1!=\"aaa\"", "true", "", False, False) ,
    ("1!=true", "true", "", False, False) , # Python evaluates this to False
    ("0!=false", "true", "", False, False) , # DPython evaluates this to False
    ("1!=nil", "true", "", False, False) ,
    ("(2+3)*4", "20", "", False, False) ,
]

@pytest.mark.parametrize("source, out_expected, err_expected, had_error, had_runtime_error", expressions)
def test_expressions(
    source: str,
    out_expected: str,
    err_expected: str,
    had_error: bool,
    had_runtime_error: bool,
    capfd: pytest.CaptureFixture[str]
) -> None:
    tokens = Scanner(source).scanTokens()
    expression = Parser(tokens).parse()
    assert expression is not None
    Interpreter().interpret(expression)

    out, err = capfd.readouterr()
    print(f"out, err = '{out}', '{err}'")
    assert out.strip() == out_expected
    assert err.strip() == err_expected
    assert LoxError.had_error is had_error
    assert LoxError.had_runtime_error is had_runtime_error
