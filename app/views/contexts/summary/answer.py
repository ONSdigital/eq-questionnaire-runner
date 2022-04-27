from flask import url_for


class Answer:
    def __init__(
        self,
        *,
        answer_schema,
        answer_value,
        block_id,
        list_name,
        list_item_id,
        return_to,
        return_to_block_id,
    ):
        self.id = answer_schema["id"]
        self.label = answer_schema.get("label")
        self.value = answer_value
        self.type = answer_schema["type"].lower()
        self.unit = answer_schema.get("unit")
        self.unit_length = answer_schema.get("unit_length")
        self.currency = answer_schema.get("currency")
        self.link = self._build_link(
            block_id=block_id,
            list_name=list_name,
            list_item_id=list_item_id,
            return_to=return_to,
            return_to_block_id=return_to_block_id,
        )

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "value": self.value,
            "type": self.type,
            "unit": self.unit,
            "unit_length": self.unit_length,
            "currency": self.currency,
            "link": self.link,
        }

    def _build_link(
        self, *, block_id, list_name, list_item_id, return_to, return_to_block_id
    ):
        return url_for(
            "questionnaire.block",
            list_name=list_name,
            block_id=block_id,
            list_item_id=list_item_id,
            return_to=return_to,
            return_to_answer_id=self.id if return_to else None,
            return_to_block_id=return_to_block_id,
            _anchor=self.id,
        )
