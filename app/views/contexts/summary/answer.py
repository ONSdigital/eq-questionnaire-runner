from typing import Mapping

from flask import url_for

from app.data_models.answer import AnswerValueEscapedTypes
from app.questionnaire.return_location import ReturnLocation

RadioCheckboxTypes = dict[str, str | AnswerValueEscapedTypes | None]
DateRangeTypes = dict[str, AnswerValueEscapedTypes | None]

InferredAnswerValueTypes = (
    None | DateRangeTypes | str | AnswerValueEscapedTypes | RadioCheckboxTypes
)


class Answer:
    def __init__(
        self,
        *,
        answer_schema: Mapping[str, str],
        answer_value: InferredAnswerValueTypes,
        block_id: str,
        list_name: str | None,
        list_item_id: str | None,
        return_location: ReturnLocation,
        is_in_repeating_section: bool,
    ) -> None:
        self.id = answer_schema["id"]
        self.label = answer_schema.get("label")
        self.value = answer_value
        self.type = answer_schema["type"].lower()
        self.unit = answer_schema.get("unit")
        self.unit_length = answer_schema.get("unit_length")
        self.currency = answer_schema.get("currency")
        self.decimal_places = answer_schema.get("decimal_places")
        self._original_answer_id = answer_schema.get("original_answer_id")
        self.link = self._build_link(
            block_id=block_id,
            list_name=list_name,
            list_item_id=list_item_id,
            return_location=return_location,
            is_in_repeating_section=is_in_repeating_section,
        )

    def serialize(self) -> dict:
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
        list_name: str | None,
        list_item_id: str | None,
        return_location: ReturnLocation,
        is_in_repeating_section: bool,
    ) -> str:
        return url_for(
            endpoint="questionnaire.block",
            list_name=list_name,
            block_id=block_id,
            list_item_id=list_item_id,
            return_to=return_location.return_to,
            return_to_answer_id=self._return_to_answer_id(
                return_to=return_location.return_to,
                list_item_id=list_item_id,
                is_in_repeating_section=is_in_repeating_section,
            ),
            return_to_block_id=return_location.return_to_block_id,
            return_to_list_item_id=return_location.return_to_list_item_id,
            _anchor=self.id,
        )

    def _return_to_answer_id(
        self,
        *,
        return_to: str | None,
        list_item_id: str | None,
        is_in_repeating_section: bool,
    ) -> str | None:
        """
        If the summary page using this answer has repeating answers, but it is not in a repeating section,
        then the answer ids will be suffixed with list item id, so the return to answer id link also needs this to work correctly
        """
        if return_to:
            if (
                list_item_id
                and not is_in_repeating_section
                and not self._original_answer_id  # original answer would mean id has already been suffixed
            ):
                return f"{self.id}-{list_item_id}"
            return self.id
