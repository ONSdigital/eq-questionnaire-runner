from typing import Any

from werkzeug.datastructures import ImmutableDict

from app.views.contexts.preview.preview_question import PreviewQuestion


class PreviewBlock:
    def __init__(
        self,
        *,
        block: ImmutableDict,
    ):
        self._block = block
        self._question = self._get_question(
            block=self._block,
        )

    @staticmethod
    def _get_question(
        block: ImmutableDict,
    ) -> dict[str, str | dict]:
        return PreviewQuestion(
            block=block,
        ).serialize()

    def serialize(self) -> dict[str, str | dict | Any]:
        return {
            "question": self._question,
        }
