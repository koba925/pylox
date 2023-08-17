import sys

from lox_runtime_error import LoxRuntimeError
from lox_token import Token
from lox_token import TokenType as TT


class LoxError:
    had_error: bool = False
    had_runtime_error: bool = False

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        LoxError.had_error = True

    @staticmethod
    def scan_error(line: int, message: str) -> None:
        LoxError.report(line, "", message)

    @staticmethod
    def parse_error(token: Token, message: str) -> None:
        if token.token_type == TT.EOF:
            LoxError.report(token.line, " at end", message)
        else:
            LoxError.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def runtime_error(error: LoxRuntimeError) -> None:
        print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
        LoxError.had_runtime_error = True
