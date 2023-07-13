from typing import Any, Mapping, Optional, Union

from flask import url_for

from app.data_models.answer import AnswerValueEscapedTypes

RadioCheckboxTypes = dict[str, Union[str, AnswerValueEscapedTypes, None]]
DateRangeTypes = dict[str, Optional[AnswerValueEscapedTypes]]

InferredAnswerValueTypes = Union[
    None, DateRangeTypes, str, AnswerValueEscapedTypes, RadioCheckboxTypes
]


class Answer:
    def __init__(
        self,
        *,
        answer_schema: Mapping[str, str],
        answer_value: InferredAnswerValueTypes,
        block_id: str,
        list_name: Optional[str],
        list_item_id: Optional[str],
        return_to: Optional[str],
        return_to_block_id: Optional[str],
    ) -> None:
        self.id = answer_schema["id"]
        self.label = answer_schema.get("label")
        self.value = answer_value
        self.type = answer_schema["type"].lower()
        self.unit = answer_schema.get("unit")
        self.unit_length = answer_schema.get("unit_length")
        self.currency = answer_schema.get("currency")
        self.decimal_places = answer_schema.get("decimal_places")
        self.link = self._build_link(
            block_id=block_id,
            list_name=list_name,
            list_item_id=list_item_id,
            return_to=return_to,
            return_to_block_id=return_to_block_id,
        )

    def serialize(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "value": self.value,
            "type": self.type,
            "unit": self.unit,
            "unit_length": self.unit_length,
            "currency": self.currency,
            "link": self.link,
            "decimal_places": self.decimal_places,
        }

    def _build_link(
        self,
        *,
        block_id: str,
        list_name: Optional[str],
        list_item_id: Optional[str],
        return_to: Optional[str],
        return_to_block_id: Optional[str],
    ) -> str:
        return url_for(
            endpoint="questionnaire.block",
            list_name=list_name,
            block_id=block_id,
            list_item_id=list_item_id,
            return_to=return_to,
            return_to_answer_id=self.id if return_to else None,
            return_to_block_id=return_to_block_id,
            _anchor=self.id,
        )
