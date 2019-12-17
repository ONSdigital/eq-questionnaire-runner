from dateutil.relativedelta import relativedelta
from werkzeug.utils import cached_property
from wtforms import StringField, Form

from app.forms.field_handlers.date_handler import DateHandler
from app.forms.validators import SingleDatePeriodCheck


class YearMonthDateHandler(DateHandler):
    DATE_FORMAT = 'yyyy-mm'

    def get_form_class(self):
        class YearMonthDateForm(Form):
            year = StringField(validators=self.validators)
            month = StringField()

            @cached_property
            def data(self):
                data = super().data

                try:
                    return '{year:04d}-{month:02d}'.format(
                        year=int(data['year']), month=int(data['month'])
                    )
                except (TypeError, ValueError):
                    return None

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
