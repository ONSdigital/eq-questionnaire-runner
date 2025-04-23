class NoTokenException(Exception):
    def __init__(self, value: str | int = "Please provide a token") -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
