#!/usr/bin/env python3

import sys

from lox_error import LoxError
from lox_scanner import Scanner


class Lox:
    @staticmethod
    def __run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token)

    @staticmethod
    def __run_file(path: str) -> None:
        with open(path) as f:
            Lox.__run(f.read())

        # Indicate an error in the exit code.
        if LoxError.had_error:
            exit(65)

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
            exit(64)
        elif len(argv) == 2:
            Lox.__run_file(argv[1])
        else:
            Lox.__run_prompt()

if __name__ == '__main__':
    Lox.main(sys.argv)
