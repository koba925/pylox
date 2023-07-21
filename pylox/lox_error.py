class LoxError:
    had_error: bool = False

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        LoxError.had_error = True

    @staticmethod
    def error(line: int, message: str) -> None:
        LoxError.report(line, "", message)
