from typing import Any, Optional

from lox_runtime_error import LoxRuntimeError
from lox_token import Token


class Environment:
    def __init__(self, enclosing: Optional["Environment"] = None) -> None:
        self.__enclosing = enclosing
        self.__values: dict[str, Any] = {}

    def get(self, name: Token) -> Any:
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]

        if self.__enclosing is not None:
            return self.__enclosing.get(name)

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.__values:
            self.__values[name.lexeme] = value
            return

        if self.__enclosing is not None:
            self.__enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name: str, value: Any) -> None:
        self.__values[name] = value

    def get_at(self, distance: int, name: str) -> Any:
        return self.__ancestor(distance).__values[name]

    def assign_at(self, distance: int, name: Token, value: Any) -> None:
        self.__ancestor(distance).__values[name.lexeme] = value

    def __ancestor(self, distance: int) -> "Environment":
        environment = self
        for _ in range(distance):
            assert environment.__enclosing is not None
            environment = environment.__enclosing

        return environment
