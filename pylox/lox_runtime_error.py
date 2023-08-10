from lox_token import Token, TokenType

class LoxRuntimeError(Exception):
    token: Token

    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = message
    
    def __str__(self) -> str:
        return f"{self.message} ({self.token})"

# raise LoxRuntimeError(Token(TokenType.NUMBER, "123", 123, 1), "Unexpected token.")
