from abc import ABC
from functools import cached_property
from typing import Any, Mapping, Optional, Union

from wtforms import Field, validators
from wtforms.validators import Optional as OptionalValidator

from app.forms.validators import ResponseRequired, format_message_with_title
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import (
    ValueSourceEscapedTypes,
    ValueSourceResolver,
    ValueSourceTypes,
)


class FieldHandler(ABC):
    MANDATORY_MESSAGE_KEY = ""

    def __init__(
        self,
        answer_schema: Mapping[str, Any],
        value_source_resolver: ValueSourceResolver,
        rule_evaluator: RuleEvaluator,
        error_messages: Mapping[str, str],
        disable_validation: bool = False,
        question_title: Optional[str] = None,
    ):
        self.answer_schema = answer_schema
        self.value_source_resolver = value_source_resolver
        self.rule_evaluator = rule_evaluator
        self.error_messages = error_messages
        self.disable_validation = disable_validation
        self.question_title = str(question_title)

        self.validation_messages: Mapping[str, str] = self.answer_schema.get(
            "validation", {}
        ).get("messages", {})

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

    def get_validation_message(self, message_key: str) -> str:
        return (
            self.validation_messages.get(message_key)
            or self.error_messages[message_key]
        )

    def get_mandatory_validator(self) -> Union[ResponseRequired, OptionalValidator]:
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
        schema_element_value: Union[ValueSourceEscapedTypes, ValueSourceTypes] = (
            schema_element["value"]
        )
        return schema_element_value

    def get_field(self) -> Field:
        pass  # pragma: no cover
