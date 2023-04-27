from decimal import Decimal
from typing import Mapping

from flask import url_for


class CalculatedSummary:
    def __init__(
        self,
        *,
        title: str | None,
        block_id: str,
        return_to: str | None,
        return_to_block_id: str | None,
        calculated_total: int | float | Decimal | None,
        answer_format: Mapping,
    ) -> None:
        self.link = self._build_link(
            block_id=block_id,
            return_to=return_to,
            return_to_block_id=return_to_block_id,
        )
        self.title = title
        self.answers = [
            {
                "id": block_id,
                "label": self.title,
                "value": calculated_total,
                "link": block_id,
                **answer_format,
            }
        ]
        self.block_id = block_id

    def serialize(self) -> dict:
        return {
            "title": self.title,
            "link": self.link,
            "id": self.block_id,
            "answers": self.answers,
        }

    @staticmethod
    def _build_link(
        *,
        block_id: str,
        return_to: str | None,
        return_to_block_id: str | None,
    ) -> str:
        return url_for(
            "questionnaire.block",
            block_id=block_id,
            return_to=return_to,
            return_to_block_id=return_to_block_id,
            calculated_summary=block_id,
        )
