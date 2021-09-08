from abc import ABC
from functools import cached_property
from typing import Any, Optional, Union

from wtforms import Field, validators

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.forms.validators import ResponseRequired, format_message_with_title
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.value_source_resolver import (
    ValueSourceEscapedTypes,
    ValueSourceResolver,
    ValueSourceTypes,
)


class FieldHandler(ABC):
    MANDATORY_MESSAGE_KEY = ""

    def __init__(
        self,
        answer_schema: dict,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore = None,
        list_store: ListStore = None,
        metadata: dict = None,
        location: Location = None,
        disable_validation: bool = False,
        question_title: str = None,
    ):
        self.schema = schema
        self.answer_schema = answer_schema
        self.error_messages = schema.error_messages or {}
        self.answer_store = answer_store or AnswerStore()
        self.list_store = list_store or ListStore()
        self.metadata = metadata or {}
        self.location = location
        self.disable_validation = disable_validation
        self.question_title = str(question_title)

        self.validation_messages = self.answer_schema.get("validation", {}).get(
            "messages", {}
        )

    @cached_property
    def value_source_resolver(self) -> ValueSourceResolver:
        list_item_id = self.location.list_item_id if self.location else None
        return ValueSourceResolver(
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            schema=self.schema,
            location=self.location,
            list_item_id=list_item_id,
            escape_answer_values=True,
        )

    @cached_property
    def validators(self) -> list[validators.Optional]:
        if not self.disable_validation:
            return [self.get_mandatory_validator()]
        return []

    @cached_property
    def label(self) -> Optional[str]:
        return self.answer_schema.get("label")

    @cached_property
    def guidance(self) -> str:
        return self.answer_schema.get("guidance", "")

    def get_validation_message(self, message_key: str) -> Optional[str]:
        return self.validation_messages.get(message_key) or self.error_messages.get(
            message_key
        )

    def get_mandatory_validator(self) -> Union[ResponseRequired, Optional[Any]]:
        if self.answer_schema["mandatory"] is True:
            mandatory_message = self.get_validation_message(self.MANDATORY_MESSAGE_KEY)

            return ResponseRequired(
                message=format_message_with_title(
                    mandatory_message, self.question_title
                )
            )
        return validators.Optional()

    def get_schema_value(
        self, schema_element: dict
    ) -> Union[ValueSourceEscapedTypes, ValueSourceTypes]:
        if isinstance(schema_element["value"], dict):
            return self.value_source_resolver.resolve(schema_element["value"])
        schema_element_value: Union[
            ValueSourceEscapedTypes, ValueSourceTypes
        ] = schema_element["value"]
        return schema_element_value

    def get_field(self) -> Field:
        pass  # pragma: no cover
