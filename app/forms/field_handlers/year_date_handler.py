from werkzeug.utils import cached_property
from wtforms import StringField, Form

from app.forms.field_handlers.date_handler import DateHandler
from app.forms.validators import SingleDatePeriodCheck


class YearDateHandler(DateHandler):
    DATE_FORMAT = 'yyyy'

    def get_form_class(self):
        class YearDateForm(Form):
            year = StringField(validators=self.validators)

            @cached_property
            def data(self):
                data = super().data

                try:
                    return '{year:04d}'.format(year=int(data['year']))
                except (TypeError, ValueError):
                    return None

        return YearDateForm

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
