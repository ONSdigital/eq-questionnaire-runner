from typing import Union

from wtforms import IntegerField, DecimalField

from app.data_model.answer_store import AnswerStore
from app.forms.fields.custom_decimal_field import CustomDecimalField
from app.forms.fields.custom_integer_field import CustomIntegerField
from app.forms.field_handlers.field_handler import FieldHandler
from app.questionnaire.location import Location
from app.validation.validators import NumberCheck, NumberRange, DecimalPlaces


class NumberHandler(FieldHandler):
    MANDATORY_MESSAGE = 'MANDATORY_TEXTFIELD'
    MAX_NUMBER = 9999999999
    MIN_NUMBER = -999999999
    MAX_DECIMAL_PLACES = 6

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
        self.dependencies = self.get_number_field_dependencies()

    @property
    def validators(self):
        validate_with = []

        if self.disable_validation is False:
            parent_validators = super().validators
            validate_with = parent_validators + self._get_number_field_validators(
                self.dependencies
            )
        return validate_with

    def get_field(self) -> Union[DecimalField, IntegerField]:
        field_type = (
            CustomDecimalField
            if self.answer_schema.get('decimal_places', 0) > 0
            else CustomIntegerField
        )
        return field_type(
            label=self.label, validators=self.validators, description=self.guidance
        )

    def get_number_field_dependencies(self):
        max_decimals = self.answer_schema.get('decimal_places', 0)

        min_value = 0

        if self.answer_schema.get('min_value'):
            min_value = self.get_value_from_schema(self.answer_schema.get('min_value'))

        max_value = self.MAX_NUMBER

        if self.answer_schema.get('max_value'):
            max_value = self.get_value_from_schema(self.answer_schema.get('max_value'))

        return {
            'max_decimals': max_decimals,
            'min_exclusive': self.answer_schema.get('min_value', {}).get(
                'exclusive', False
            ),
            'max_exclusive': self.answer_schema.get('max_value', {}).get(
                'exclusive', False
            ),
            'min_value': min_value,
            'max_value': max_value,
        }

    def _get_number_field_validators(self, dependencies):
        answer_errors = self.error_messages.copy()

        if (
            'validation' in self.answer_schema
            and 'messages' in self.answer_schema['validation']
        ):
            for error_key, error_message in self.answer_schema['validation'][
                'messages'
            ].items():
                answer_errors[error_key] = error_message

        return [
            NumberCheck(answer_errors['INVALID_NUMBER']),
            NumberRange(
                minimum=dependencies['min_value'],
                minimum_exclusive=dependencies['min_exclusive'],
                maximum=dependencies['max_value'],
                maximum_exclusive=dependencies['max_exclusive'],
                messages=answer_errors,
                currency=self.answer_schema.get('currency'),
            ),
            DecimalPlaces(
                max_decimals=dependencies['max_decimals'], messages=answer_errors
            ),
        ]

    def get_value_from_schema(self, definition):
        if 'value' in definition:
            return definition['value']

        source_answer_id = definition.get('answer_id')
        answer = self.answer_store.get_answer(source_answer_id)

        return answer.value if answer else None
