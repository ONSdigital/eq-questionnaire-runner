from dateutil.relativedelta import relativedelta

from app.forms.field_handlers.date_handler import DateHandler
from app.forms.fields.month_year_date_field import MonthYearDateField
from app.forms.validators import SingleDatePeriodCheck


class MonthYearDateHandler(DateHandler):
    DATE_FORMAT = 'yyyy-mm'

    def get_field(self) -> MonthYearDateField:
        return MonthYearDateField(
            self.validators, label=self.label, description=self.guidance
        )

    def get_min_max_validator(self, minimum_date, maximum_date):
        messages = self.answer_schema.get('validation', {}).get('messages')

        display_format = 'MMMM yyyy'
        minimum_date = (
            minimum_date.replace(day=1) if minimum_date else None
        )  # First day of Month
        maximum_date = (
            maximum_date + relativedelta(day=31) if maximum_date else None
        )  # Last day of month

        return SingleDatePeriodCheck(
            messages=messages,
            date_format=display_format,
            minimum_date=minimum_date,
            maximum_date=maximum_date,
        )
