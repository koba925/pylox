from typing import Any, Optional


class ReturnException(Exception):
    def __init__(self, value: Optional[Any]) -> None:
        super().__init__()
        self.value = value
