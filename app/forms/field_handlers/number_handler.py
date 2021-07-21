from functools import cached_property
from typing import Union

from wtforms import DecimalField, IntegerField

from app.data_models.answer_store import AnswerStore
from app.forms.field_handlers.field_handler import FieldHandler
from app.forms.fields import DecimalFieldWithSeparator, IntegerFieldWithSeparator
from app.forms.validators import DecimalPlaces, NumberCheck, NumberRange
from app.questionnaire import Location
from app.settings import MAX_NUMBER


class NumberHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_NUMBER"

    def __init__(
        self,
        answer_schema: dict,
        error_messages: dict = None,
        answer_store: AnswerStore = None,
        metadata: dict = None,
        location: Location = None,
        disable_validation: bool = False,
        question_title: str = None,
    ):
        super().__init__(
            answer_schema,
            error_messages,
            answer_store,
            metadata,
            location,
            disable_validation,
            question_title,
        )
        self.references = self.get_field_references()

    @cached_property
    def max_decimals(self):
        return self.answer_schema.get("decimal_places", 0)

    @cached_property
    def validators(self):
        validate_with = []
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

    def get_field_references(self):
        schema_minimum = self.answer_schema.get("minimum", {})
        schema_maximum = self.answer_schema.get("maximum", {})

        minimum = self.get_schema_value(schema_minimum) if schema_minimum else 0
        maximum = (
            self.get_schema_value(schema_maximum) if schema_maximum else MAX_NUMBER
        )

        return {
            "min_exclusive": schema_minimum.get("exclusive", False),
            "max_exclusive": schema_maximum.get("exclusive", False),
            "minimum": minimum,
            "maximum": maximum,
        }

    def _get_number_field_validators(self):
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
