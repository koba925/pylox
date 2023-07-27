from lox_token import Token, TokenType


class LoxError:
    had_error: bool = False

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        LoxError.had_error = True

    @staticmethod
    def parse_error(token: Token, message: str) -> None:
        if token.token_type == TokenType.EOF:
            LoxError.report(token.line, " at end", message)
        else:
            LoxError.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def scan_error(line: int, message: str) -> None:
        LoxError.report(line, "", message)
