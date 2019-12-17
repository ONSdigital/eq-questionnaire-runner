from wtforms import StringField

from app.forms.date_form import DateForm
from app.forms.field_handlers.date_handler import DateHandler
from app.forms.validators import SingleDatePeriodCheck


class YearDateHandler(DateHandler):
    DATE_FORMAT = 'yyyy'

    def get_form_class(self):
        class CustomDateForm(DateForm):
            pass

        CustomDateForm.year = StringField(validators=self.validators)

        return CustomDateForm

    def get_min_max_validator(self, minimum_date, maximum_date):
        messages = self.answer_schema.get('validation', {}).get('messages')

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
