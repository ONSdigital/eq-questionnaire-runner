from werkzeug.datastructures import MultiDict
from wtforms import FormField

from app.forms.custom_fields import CustomDecimalField, CustomIntegerField
from app.forms.date_form import DateFormType, DateField, get_date_limits
from app.forms.duration_form import get_duration_form
from app.forms.fields import (
    get_number_field_dependencies,
    get_number_field_validators,
    get_select_field,
    get_string_field,
    get_text_area_field,
    get_dropdown_field,
    get_select_multiple_field,
)


class FieldFactory:
    def __init__(
        self,
        answer,
        label,
        error_messages,
        answer_store,
        metadata,
        disable_validation=False,
    ):
        self.answer = answer
        self.label = label
        self.error_messages = error_messages
        self.answer_store = answer_store
        self.metadata = metadata
        self.disable_validation = disable_validation

    def get_field(self):
        guidance = self.answer.get('guidance', '')

        date_field_types = {
            'Date': DateFormType.YearMonthDay,
            'MonthYearDate': DateFormType.YearMonth,
            'YearDate': DateFormType.Year,
        }

        if self.answer['type'] in ['Number', 'Currency', 'Percentage', 'Unit']:
            dependencies = get_number_field_dependencies(self.answer, self.answer_store)
            validate_with = get_number_field_validators(
                self.answer, dependencies, self.error_messages, self.disable_validation
            )
            field_type = (
                CustomDecimalField
                if self.answer.get('decimal_places', 0) > 0
                else CustomIntegerField
            )
            field = field_type(
                label=self.label, validators=validate_with, description=guidance
            )
        elif self.answer['type'] in date_field_types:
            minimum_date, maximum_date = get_date_limits(
                self.answer, self.answer_store, self.metadata
            )
            field = DateField(
                date_field_types[self.answer['type']],
                minimum_date,
                maximum_date,
                self.answer,
                self.error_messages,
                label=self.label,
                description=guidance,
            )
        elif self.answer['type'] == 'Duration':
            field = FormField(
                get_duration_form(self.answer, self.error_messages),
                label=self.label,
                description=guidance,
            )
        else:
            field = {
                'Checkbox': get_select_multiple_field,
                'Radio': get_select_field,
                'Relationship': get_select_field,
                'TextArea': get_text_area_field,
                'TextField': get_string_field,
                'Dropdown': get_dropdown_field,
            }[self.answer['type']](
                self.answer,
                self.label,
                guidance,
                self.error_messages,
                self.disable_validation,
            )

        return field

    def _option_value_in_data(self, option, data):
        if isinstance(data, MultiDict):
            return option['value'] in data.to_dict(flat=False).get(
                self.answer['id'], []
            )

        return option['value'] in dict(data).get(self.answer['id'], [])

    def get_option_field(self, option, data):
        disable_validation = not self._option_value_in_data(option, data)
        detail_answer = option['detail_answer']
        detail_answer_error_messages = (
            detail_answer['validation']['messages']
            if detail_answer.get('validation')
            else self.error_messages
        )

        field_factory = FieldFactory(
            detail_answer,
            detail_answer.get('label'),
            detail_answer_error_messages,
            self.answer_store,
            self.metadata,
            disable_validation=disable_validation,
        )
        return field_factory.get_field()
