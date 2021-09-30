from functools import cached_property
from typing import Any, Union

from wtforms import DecimalField, IntegerField

from app.forms.field_handlers.field_handler import FieldHandler
from app.forms.fields import DecimalFieldWithSeparator, IntegerFieldWithSeparator
from app.forms.validators import (
    DecimalPlaces,
    NumberCheck,
    NumberRange,
    ResponseRequired,
)
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.settings import MAX_NUMBER

NumberValidatorTypes = list[
    Union[ResponseRequired, NumberCheck, NumberRange, DecimalPlaces]
]


class NumberHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_NUMBER"

    def __init__(
        self,
        answer_schema: dict,
        value_source_resolver: ValueSourceResolver,
        error_messages: dict[str, str],
        disable_validation: bool = False,
        question_title: str = None,
    ):
        super().__init__(
            answer_schema,
            value_source_resolver,
            error_messages,
            disable_validation,
            question_title,
        )
        self.references = self.get_field_references()

    @cached_property
    def max_decimals(self) -> int:
        return self.answer_schema.get("decimal_places", 0)

    @cached_property
    def validators(
        self,
    ) -> NumberValidatorTypes:
        validate_with: NumberValidatorTypes = []
        if self.disable_validation is False:
            validate_with = super().validators + self._get_number_field_validators()
        return validate_with

    def get_field(self) -> Union[DecimalField, IntegerField]:
        field_type = (
            DecimalFieldWithSeparator
            if self.max_decimals > 0
            else IntegerFieldWithSeparator
        )
        return field_type(
            label=self.label, validators=self.validators, description=self.guidance
        )

    def get_field_references(
        self,
    ) -> dict[str, Any]:

        schema_minimum: dict = self.answer_schema.get("minimum", {})
        schema_maximum: dict = self.answer_schema.get("maximum", {})

        min_exclusive: bool = schema_minimum.get("exclusive", False)
        max_exclusive: bool = schema_maximum.get("exclusive", False)

        minimum = self.get_schema_value(schema_minimum) if schema_minimum else 0
        maximum = (
            self.get_schema_value(schema_maximum) if schema_maximum else MAX_NUMBER
        )

        return {
            "min_exclusive": min_exclusive,
            "max_exclusive": max_exclusive,
            "minimum": minimum,
            "maximum": maximum,
        }

    def _get_number_field_validators(
        self,
    ) -> list[Union[NumberCheck, NumberRange, DecimalPlaces]]:
        answer_errors = self.error_messages.copy()

        for error_key in self.validation_messages.keys():
            answer_errors[error_key] = self.get_validation_message(error_key)

        return [
            NumberCheck(answer_errors["INVALID_NUMBER"]),
            NumberRange(
                minimum=self.references["minimum"],
                minimum_exclusive=self.references["min_exclusive"],
                maximum=self.references["maximum"],
                maximum_exclusive=self.references["max_exclusive"],
                messages=answer_errors,
                currency=self.answer_schema.get("currency"),
            ),
            DecimalPlaces(max_decimals=self.max_decimals, messages=answer_errors),
        ]
