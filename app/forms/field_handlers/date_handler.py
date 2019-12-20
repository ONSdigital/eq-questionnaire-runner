from datetime import datetime

from dateutil.relativedelta import relativedelta
from werkzeug.utils import cached_property

from app.forms.field_handlers.field_handler import FieldHandler
from app.forms.fields.date_field import DateField
from app.questionnaire.rules import convert_to_datetime
from app.forms.validators import (
    SingleDatePeriodCheck,
    OptionalForm,
    DateCheck,
    DateRequired,
)


class DateHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_DATE"
    DATE_FORMAT = "yyyy-mm-dd"
    DISPLAY_FORMAT = "d MMMM yyyy"

    @cached_property
    def validators(self):
        validate_with = [OptionalForm()]

        if self.answer_schema["mandatory"] is True:
            validate_with = [
                DateRequired(
                    message=self.get_validation_message(self.MANDATORY_MESSAGE_KEY)
                )
            ]

        error_message = self.get_validation_message("INVALID_DATE")

        validate_with.append(DateCheck(error_message))

        minimum_date = self.get_date_value("minimum")
        maximum_date = self.get_date_value("maximum")

        if minimum_date or maximum_date:
            min_max_validator = self.get_min_max_validator(minimum_date, maximum_date)
            validate_with.append(min_max_validator)

        return validate_with

    def get_field(self) -> DateField:
        return DateField(self.validators, label=self.label, description=self.guidance)

    def get_min_max_validator(self, minimum_date, maximum_date):
        messages = self.answer_schema.get("validation", {}).get("messages")

        return SingleDatePeriodCheck(
            messages=messages,
            date_format=self.DISPLAY_FORMAT,
            minimum_date=minimum_date,
            maximum_date=maximum_date,
        )

    def get_referenced_date(self, key):
        """
        Gets value of the referenced date type, whether it is a value,
        id of an answer or a meta date.

        :return: date value
        """
        value = self.get_schema_value(self.answer_schema[key])

        if value == "now":
            value = datetime.utcnow().strftime("%Y-%m-%d")

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
            years=offset.get("years", 0),
            months=offset.get("months", 0),
            days=offset.get("days", 0),
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

            if "offset_by" in self.answer_schema[key]:
                offset = self.answer_schema[key]["offset_by"]
                date_value = self.transform_date_by_offset(date_value, offset)

        return date_value
