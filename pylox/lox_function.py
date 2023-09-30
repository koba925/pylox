from typing import Any, TYPE_CHECKING

from lox_callable import LoxCallable
from lox_stmt import Function
from lox_environment import Environment
from lox_return import ReturnException

if TYPE_CHECKING:
    from lox_interpreter import Interpreter


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment) -> None:
        self.__declaration = declaration
        self.__closure = closure

    def arity(self) -> int:
        return len(self.__declaration.params)

    def call(self, interpreter: "Interpreter", arguments: list[Any]) -> Any:
        environment = Environment(self.__closure)
        for param, arg in zip(self.__declaration.params, arguments):
            environment.define(param.lexeme, arg)

        try:
            interpreter.execute_block(self.__declaration.body, environment)
        except ReturnException as r:
            return r.value

        return None

    def __str__(self) -> str:
        return "<fn " + self.__declaration.name.lexeme + ">"
