from datetime import datetime

from dateutil.relativedelta import relativedelta
from werkzeug.utils import cached_property

from app.forms.date_form import DateFormType, DateField
from app.forms.handlers.string_handler import StringHandler
from app.questionnaire.rules import (
    get_answer_value,
    convert_to_datetime,
    get_metadata_value,
)
from app.utilities.schema import load_schema_from_metadata
from app.validation.validators import (
    SingleDatePeriodCheck,
    OptionalForm,
    DateCheck,
    DateRequired,
)


class DateHandler(StringHandler):
    MANDATORY_MESSAGE = 'MANDATORY_RADIO'
    DATE_FIELD_MAP = {
        'Date': DateFormType.YearMonthDay,
        'MonthYearDate': DateFormType.YearMonth,
        'YearDate': DateFormType.Year,
    }

    @cached_property
    def form_type(self):
        return self.DATE_FIELD_MAP[self.answer_type]

    @cached_property
    def validators(self):
        minimum_date, maximum_date = self.get_date_limits()

        validate_with = [OptionalForm()]

        if self.answer['mandatory'] is True:
            validate_with = self.validate_mandatory_date()

        error_message = self.get_bespoke_message('INVALID_DATE')

        validate_with.append(DateCheck(error_message))

        if minimum_date or maximum_date:
            messages = None
            if 'validation' in self.answer:
                messages = self.answer['validation'].get('messages')
            min_max_validation = self.validate_min_max_date(
                minimum_date,
                maximum_date,
                messages,
                self.form_type.value['date_format'],
            )
            validate_with.append(min_max_validation)

        return validate_with

    def get_field(self):
        return DateField(
            self.DATE_FIELD_MAP[self.answer_type],
            self.validators,
            label=self.label,
            description=self.guidance,
        )

    def validate_mandatory_date(self):
        error_message = (
            self.get_bespoke_message('MANDATORY_DATE')
            or self.error_messages['MANDATORY_DATE']
        )

        validate_with = [DateRequired(message=error_message)]
        return validate_with

    def get_bespoke_message(self, message_type):
        if (
            'validation' in self.answer
            and 'messages' in self.answer['validation']
            and message_type in self.answer['validation']['messages']
        ):
            return self.answer['validation']['messages'][message_type]

        return None

    @staticmethod
    def validate_min_max_date(minimum_date, maximum_date, messages, date_format):
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

    def get_referenced_date(self, limit):
        """
        Gets value of the referenced date type, whether it is a value,
        id of an answer or a meta date.

        :return: date value
        """
        value = None
        referenced_date = self.answer[limit]

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

    def get_date_limits(self):
        """
        Gets attributes within a minimum or maximum of a date field and validates that the entered date
        is valid.

        :return: attributes
        """
        date_references = {'minimum': None, 'maximum': None}

        for limit in date_references:
            if limit in self.answer:
                date_references[limit] = self.get_referenced_date(limit)

                if 'offset_by' in self.answer[limit]:
                    offset = self.answer[limit]['offset_by']
                    date_references[limit] = DateHandler.transform_date_by_offset(
                        date_references[limit], offset
                    )

        # Extra runtime validation that will catch invalid schemas
        # Similar validation in schema validator
        if date_references['minimum'] and date_references['maximum']:
            if date_references['minimum'] > date_references['maximum']:
                raise Exception(
                    'The minimum offset date is greater than the maximum offset date for {}.'.format(
                        self.answer['id']
                    )
                )

        return date_references['minimum'], date_references['maximum']
