from typing import Generator

import pytest
from lox_error import LoxError
from lox_interpreter import Interpreter
from lox_parser import Parser
from lox_scanner import Scanner


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
    ("var a = 1; print a;", "1", "", False, False),
    ("var a; print a;", "nil", "", False, False),
    ("var a = 1; var b = 2; print a + b;", "3", "", False, False),
    ("var a = 1; print a = 2; print a;", "2\n2", "", False, False),
    (
        'print a; var a = "too late!";',
        "",
        "Undefined variable 'a'.\n[line 1]",
        False,
        True,
    ),
    (
        "a = 1;",
        "",
        "Undefined variable 'a'.\n[line 1]",
        False,
        True,
    ),
    (
        "{var a = 1; print a;}",
        "1",
        "",
        False,
        False,
    ),
    (
        "{} print 1;",
        "1",
        "",
        False,
        False,
    ),
    (
        "{var a = 1; print a;",
        "",
        "[line 1] Error at end: Expect '}' after block.",
        True,
        False,
    ),
    (
        """\
        {
        var a = "first";
        print a; // "first".
        }

        {
        var a = "second";
        print a; // "second".
        }
        """,
        "first\nsecond",
        "",
        False,
        False,
    ),
    (
        """\
        // How loud?
        var volume = 11;

        // Silence.
        volume = 0;

        // Calculate size of 3x4x5 cuboid.
        {
        var volume = 3 * 4 * 5;
        print volume;
        }

        print volume;
        """,
        "60\n0",
        "",
        False,
        False,
    ),
    (
        """\
        var global = "outside";
        {
        var local = "inside";
        print global + local;
        }
        """,
        "outsideinside",
        "",
        False,
        False,
    ),
    (
        """\
        var a = "global a";
        var b = "global b";
        var c = "global c";
        {
        var a = "outer a";
        var b = "outer b";
        {
            var a = "inner a";
            print a;
            print b;
            print c;
        }
        print a;
        print b;
        print c;
        }
        print a;
        print b;
        print c;
        """,
        """\
inner a
outer b
global c
outer a
outer b
global c
global a
global b
global c""",
        "",
        False,
        False,
    ),
    (
        """\
        {
        var a = "in block";
        }
        print a; // Error! No more "a".
        """,
        "",
        "Undefined variable 'a'.\n[line 4]",
        False,
        True,
    ),
    (
        "if (true) print 1; else print 2;",
        "1",
        "",
        False,
        False,
    ),
    (
        "if (false) print 1; else print 2;",
        "2",
        "",
        False,
        False,
    ),
    (
        "if (false) print 1; else if (true) print 2; else print 3;",
        "2",
        "",
        False,
        False,
    ),
    (
        "if (false) print 1; else if (false) print 2; else print 3;",
        "3",
        "",
        False,
        False,
    ),
    (
        "if false) print 1; else print 2;",
        "",
        "[line 1] Error at 'false': Expect '(' after 'if'.",
        True,
        False,
    ),
    (
        "if (false print 1; else print 2;",
        "",
        "[line 1] Error at 'print': Expect ')' after if condition.",
        True,
        False,
    ),
    # (
    #     """\
    #     fun isOdd(n) {
    #         if (n == 0) return false;
    #         return isEven(n - 1);
    #     }
    #     fun isEven(n) {
    #         if (n == 0) return true;
    #         return isOdd(n - 1);
    #     }
    #     print isOdd(2);
    #     print isOdd(3);
    #     print isEven(2);
    #     print isEven(3);
    #     """,
    #     "",
    #     "",
    #     False,
    #     False,
    # ),
    # (
    #     """\
    #     class Saxophone {
    #     play() {
    #         print "Careless Whisper";
    #     }
    #     }
    #     class GolfClub {
    #     play() {
    #         print "Fore!";
    #     }
    #     }
    #     fun playIt(thing) {
    #     thing.play();
    #     }
    #     print playIt(Saxophone())
    #     print playIt(GolfClub())
    #     """,
    #     "Careless Whisper\nFore!",
    #     "",
    #     False,
    #     False,
    # ),
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
    assert LoxError.had_error is had_error
    if not had_error:
        assert stmts is not None
        Interpreter().interpret(stmts)

    out, err = capfd.readouterr()
    print(f"out, err = '{out}', '{err}'")
    assert out.strip() == out_expected
    assert err.strip().startswith(err_expected)
    assert LoxError.had_error is had_error
    assert LoxError.had_runtime_error is had_runtime_error
