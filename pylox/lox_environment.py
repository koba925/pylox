from typing import Any

from lox_runtime_error import LoxRuntimeError
from lox_token import Token


class Environment:
    def __init__(self) -> None:
        self.__values: dict[str, Any] = {}

    def get(self, name: Token) -> Any:
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.__values:
            self.__values[name.lexeme] = value
        else:
            raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name: str, value: Any) -> None:
        self.__values[name] = value
