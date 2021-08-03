from typing import Union


class NoQuestionnaireStateException(Exception):
    def __init__(self, value: Union[str, int]) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
