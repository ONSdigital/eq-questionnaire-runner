from datetime import datetime

from dateutil.relativedelta import relativedelta
from werkzeug.utils import cached_property

from app.forms.date_form import DateFormType, DateField
from app.forms.field_handlers.field_handler import FieldHandler
from app.questionnaire.rules import (
    get_answer_value,
    convert_to_datetime,
    get_metadata_value,
)
from app.utilities.schema import load_schema_from_metadata
from app.forms.validators import (
    SingleDatePeriodCheck,
    OptionalForm,
    DateCheck,
    DateRequired,
)


class DateHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = 'MANDATORY_DATE'
    DATE_FIELD_MAP = {
        'Date': DateFormType.YearMonthDay,
        'MonthYearDate': DateFormType.YearMonth,
        'YearDate': DateFormType.Year,
    }
    DATE_FORMAT_MAP = {
        DateFormType.YearMonthDay: 'yyyy-mm-dd',
        DateFormType.YearMonth: 'yyyy-mm',
        DateFormType.Year: 'yyyy',
    }

    @cached_property
    def form_type(self):
        return self.DATE_FIELD_MAP[self.answer_type]

    @cached_property
    def validators(self):
        validate_with = [OptionalForm()]

        if self.answer_schema['mandatory'] is True:
            validate_with = [
                DateRequired(message=self.get_validation_message('MANDATORY_DATE'))
            ]

        error_message = self.get_validation_message('INVALID_DATE')

        validate_with.append(DateCheck(error_message))

        minimum_date = self.get_date_value('minimum')
        maximum_date = self.get_date_value('maximum')

        if minimum_date or maximum_date:
            min_max_validator = self.get_min_max_validator(minimum_date, maximum_date)
            validate_with.append(min_max_validator)

        return validate_with

    def get_field(self) -> DateField:
        return DateField(
            self.form_type, self.validators, label=self.label, description=self.guidance
        )

    def get_min_max_validator(self, minimum_date, maximum_date):
        messages = self.answer_schema.get('validation', {}).get('messages')
        date_format = self.DATE_FORMAT_MAP[self.form_type]
        display_format = 'd MMMM yyyy'

        if date_format == 'yyyy-mm':
            display_format = 'MMMM yyyy'
            minimum_date = (
                minimum_date.replace(day=1) if minimum_date else None
            )  # First day of Month
            maximum_date = (
                maximum_date + relativedelta(day=31) if maximum_date else None
            )  # Last day of month
        elif date_format == 'yyyy':
            display_format = 'yyyy'
            minimum_date = (
                minimum_date.replace(month=1, day=1) if minimum_date else None
            )  # January 1st
            maximum_date = (
                maximum_date.replace(month=12, day=31) if maximum_date else None
            )  # Last day of december

        return SingleDatePeriodCheck(
            messages=messages,
            date_format=display_format,
            minimum_date=minimum_date,
            maximum_date=maximum_date,
        )

    def get_referenced_date(self, key):
        """
        Gets value of the referenced date type, whether it is a value,
        id of an answer or a meta date.

        :return: date value
        """
        value = None
        referenced_date = self.answer_schema[key]

        if 'value' in referenced_date:
            if referenced_date['value'] == 'now':
                value = datetime.utcnow().strftime('%Y-%m-%d')
            else:
                value = referenced_date['value']
        elif 'meta' in referenced_date:
            value = get_metadata_value(self.metadata, referenced_date['meta'])
        elif 'answer_id' in referenced_date:
            schema = load_schema_from_metadata(self.metadata)
            answer_id = referenced_date['answer_id']
            list_item_id = self.location.list_item_id if self.location else None

            value = get_answer_value(
                answer_id, self.answer_store, schema, list_item_id=list_item_id
            )

        return convert_to_datetime(value)

    @staticmethod
    def transform_date_by_offset(date_to_offset, offset):
        """
        Adds/subtracts offset from a date and returns
        the new offset value

        :param date_to_offset: The date to offset
        :param offset: The object which contains the offset.
        :return: date value
        """
        date_to_offset += relativedelta(
            years=offset.get('years', 0),
            months=offset.get('months', 0),
            days=offset.get('days', 0),
        )

        return date_to_offset

    def get_date_value(self, key):
        """
        Gets attributes within a minimum or maximum of a date field and validates that the entered date
        is valid.

        :return: attributes
        """
        date_value = None

        if key in self.answer_schema:
            date_value = self.get_referenced_date(key)

            if 'offset_by' in self.answer_schema[key]:
                offset = self.answer_schema[key]['offset_by']
                date_value = self.transform_date_by_offset(date_value, offset)

        return date_value
