class Outer:
    class Inner(Outer):
        def __init__(self) -> None:
            super().__init__()
