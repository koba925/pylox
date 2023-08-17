from lox_token import Token


class LoxRuntimeError(Exception):
    token: Token

    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = message

    def __str__(self) -> str:
        return f"{self.message} ({self.token})"
