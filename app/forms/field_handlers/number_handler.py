from typing import Union

from werkzeug.utils import cached_property
from wtforms import IntegerField, DecimalField

from app.data_model.answer_store import AnswerStore
from app.forms.fields.decimal_field_with_separator import DecimalFieldWithSeparator
from app.forms.fields.integer_field_with_separator import IntegerFieldWithSeparator
from app.forms.field_handlers.field_handler import FieldHandler
from app.questionnaire.location import Location
from app.forms.validators import NumberCheck, NumberRange, DecimalPlaces


class NumberHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = 'MANDATORY_NUMBER'
    MAX_NUMBER = 9999999999

    def __init__(
        self,
        answer_schema: dict,
        error_messages: dict = None,
        answer_store: AnswerStore = None,
        metadata: dict = None,
        location: Location = None,
        disable_validation: bool = False,
    ):
        super().__init__(
            answer_schema,
            error_messages,
            answer_store,
            metadata,
            location,
            disable_validation,
        )
        self.references = self.get_field_references()

    @cached_property
    def max_decimals(self):
        return self.answer_schema.get('decimal_places', 0)

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
        schema_min_value = self.answer_schema.get('min_value', {})
        schema_max_value = self.answer_schema.get('max_value', {})

        min_value = self.get_schema_value(schema_min_value) if schema_min_value else 0
        max_value = (
            self.get_schema_value(schema_max_value)
            if schema_max_value
            else self.MAX_NUMBER
        )

        return {
            'min_exclusive': schema_min_value.get('exclusive', False),
            'max_exclusive': schema_max_value.get('exclusive', False),
            'min_value': min_value,
            'max_value': max_value,
        }

    def _get_number_field_validators(self):
        answer_errors = self.error_messages.copy()
        schema_validation_messages = self.answer_schema.get('validation', {}).get(
            'messages', {}
        )

        for error_key, error_message in schema_validation_messages.items():
            answer_errors[error_key] = error_message

        return [
            NumberCheck(answer_errors['INVALID_NUMBER']),
            NumberRange(
                minimum=self.references['min_value'],
                minimum_exclusive=self.references['min_exclusive'],
                maximum=self.references['max_value'],
                maximum_exclusive=self.references['max_exclusive'],
                messages=answer_errors,
                currency=self.answer_schema.get('currency'),
            ),
            DecimalPlaces(max_decimals=self.max_decimals, messages=answer_errors),
        ]
