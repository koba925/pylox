#!/usr/bin/env python3

import sys

from lox_error import LoxError
from lox_scanner import Scanner
from lox_parser import Parser
from lox_ast_printer import AstPrinter
from lox_interpreter import Interpreter

# from lox_ast_printer import AstPrinter


class Lox:
    interpreter = Interpreter()

    @staticmethod
    def __run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()

        # print("Tokens:", *tokens, sep="\n")

        parser = Parser(tokens)
        statements = parser.parse()

        # Stop if there was a syntax error.
        if LoxError.had_error:
            return

        # Check expression is not none to avoid mypy error.
        assert statements is not None

        print("AST:")
        print(AstPrinter().print(statements))
        Lox.interpreter.interpret(statements)

    @staticmethod
    def __run_file(path: str) -> None:
        with open(path, encoding="utf-8") as f:
            Lox.__run(f.read())

        # Indicate an error in the exit code.
        if LoxError.had_error:
            sys.exit(65)
        if LoxError.had_runtime_error:
            sys.exit(70)

    @staticmethod
    def __run_prompt() -> None:
        while True:
            try:
                line = input("> ")
            except EOFError:
                print()
                break
            Lox.__run(line)
            LoxError.had_error = False

    @staticmethod
    def main(argv: list[str]) -> None:
        if len(argv) > 2:
            print("Usage: main.py")
            sys.exit(64)
        elif len(argv) == 2:
            Lox.__run_file(argv[1])
        else:
            Lox.__run_prompt()


if __name__ == "__main__":
    Lox.main(sys.argv)
