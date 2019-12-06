from decimal import Decimal

from app.forms.custom_fields import CustomDecimalField, CustomIntegerField
from app.forms.handlers.field_handler import FieldHandler
from app.validation.validators import NumberCheck, NumberRange, DecimalPlaces


class NumberHandler(FieldHandler):
    MAX_NUMBER = 9999999999
    MIN_NUMBER = -999999999
    MAX_DECIMAL_PLACES = 6

    def __init__(
        self,
        answer,
        error_messages,
        answer_store,
        metadata,
        location,
        disable_validation=False,
    ):
        super().__init__(
            answer, error_messages, answer_store, metadata, location, disable_validation
        )
        self.dependencies = self.get_number_field_dependencies()

    @property
    def validators(self):
        validate_with = []

        if self.disable_validation is False:
            self.check_number_field_dependencies(self.dependencies)

            validate_with = self._get_number_field_validators(self.dependencies)
        return validate_with

    def get_field(self):
        field_type = (
            CustomDecimalField
            if self.answer.get('decimal_places', 0) > 0
            else CustomIntegerField
        )
        return field_type(
            label=self.label, validators=self.validators, description=self.guidance
        )

    def get_number_field_dependencies(self):
        max_decimals = self.answer.get('decimal_places', 0)

        min_value = 0

        if self.answer.get('min_value'):
            min_value = self.get_schema_defined_limit(
                self.answer['id'], self.answer.get('min_value')
            )

        max_value = self.MAX_NUMBER

        if self.answer.get('max_value'):
            max_value = self.get_schema_defined_limit(
                self.answer['id'], self.answer.get('max_value')
            )

        return {
            'max_decimals': max_decimals,
            'min_exclusive': self.answer.get('min_value', {}).get('exclusive', False),
            'max_exclusive': self.answer.get('max_value', {}).get('exclusive', False),
            'min_value': min_value,
            'max_value': max_value,
        }

    def _get_number_field_validators(self, dependencies):
        answer_errors = self.error_messages.copy()

        if 'validation' in self.answer and 'messages' in self.answer['validation']:
            for error_key, error_message in self.answer['validation'][
                'messages'
            ].items():
                answer_errors[error_key] = error_message

        mandatory_or_optional = self.get_mandatory_validator('MANDATORY_NUMBER')

        return mandatory_or_optional + [
            NumberCheck(answer_errors['INVALID_NUMBER']),
            NumberRange(
                minimum=dependencies['min_value'],
                minimum_exclusive=dependencies['min_exclusive'],
                maximum=dependencies['max_value'],
                maximum_exclusive=dependencies['max_exclusive'],
                messages=answer_errors,
                currency=self.answer.get('currency'),
            ),
            DecimalPlaces(
                max_decimals=dependencies['max_decimals'], messages=answer_errors
            ),
        ]

    def check_number_field_dependencies(self, dependencies):
        if dependencies['max_decimals'] > self.MAX_DECIMAL_PLACES:
            raise Exception(
                'decimal_places: {} > system maximum: {} for answer id: {}'.format(
                    dependencies['max_decimals'],
                    self.MAX_DECIMAL_PLACES,
                    self.answer['id'],
                )
            )

        if dependencies['min_value'] < self.MIN_NUMBER:
            raise Exception(
                'min_value: {} < system minimum: {} for answer id: {}'.format(
                    dependencies['min_value'], self.MIN_NUMBER, self.answer['id']
                )
            )

        if dependencies['max_value'] > self.MAX_NUMBER:
            raise Exception(
                'max_value: {} > system maximum: {} for answer id: {}'.format(
                    dependencies['max_value'], self.MAX_NUMBER, self.answer['id']
                )
            )

        if dependencies['min_value'] > dependencies['max_value']:
            raise Exception(
                'min_value: {} > max_value: {} for answer id: {}'.format(
                    dependencies['min_value'],
                    dependencies['max_value'],
                    self.answer['id'],
                )
            )

    def get_schema_defined_limit(self, answer_id, definition):
        if 'value' in definition:
            return definition['value']

        source_answer_id = definition.get('answer_id')
        answer = self.answer_store.get_answer(source_answer_id)
        value = answer.value

        if not isinstance(value, int) and not isinstance(value, Decimal):
            raise Exception(
                'answer: {} value: {} for answer id: {} is not a valid number'.format(
                    source_answer_id, value, answer_id
                )
            )

        return value
