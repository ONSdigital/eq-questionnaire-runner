from dateutil.relativedelta import relativedelta
from wtforms import StringField

from app.forms.date_form import DateForm
from app.forms.field_handlers.date_handler import DateHandler
from app.forms.validators import SingleDatePeriodCheck


class YearMonthDateHandler(DateHandler):
    DATE_FORMAT = 'yyyy-mm'

    def get_form_class(self):
        class YearMonthDateForm(DateForm):
            year = StringField(validators=self.validators)
            month = StringField()

        return YearMonthDateForm

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
