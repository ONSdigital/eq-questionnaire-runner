from typing import Any, Union

from werkzeug.datastructures import ImmutableDict

from app.views.contexts.preview.preview_question import PreviewQuestion


class PreviewBlock:
    def __init__(
        self,
        *,
        block: ImmutableDict,
    ):
        self.block = block
        self.question = self.get_question(
            block=self.block,
        )

    @staticmethod
    def get_question(
        block: ImmutableDict,
    ) -> dict[str, Union[str, dict]]:
        return PreviewQuestion(
            block=block,
        ).serialize()

    def serialize(self) -> dict[str, Union[str, dict, Any]]:
        return {
            "question": self.question,
        }
