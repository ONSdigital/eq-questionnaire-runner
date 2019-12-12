import logging

from enum import Enum

from werkzeug.utils import cached_property
from wtforms import Form, StringField, FormField

logger = logging.getLogger(__name__)


class DateFormType(Enum):
    YearMonthDay = 1
    YearMonth = 2
    Year = 3


class DateField(FormField):
    def __init__(self, date_form_type: DateFormType, validators, **kwargs):
        form_class = get_form(date_form_type, validators)
        super().__init__(form_class, **kwargs)

    def process(self, formdata, data=None):
        if data is not None:
            substrings = data.split('-')
            if len(substrings) == 3:
                data = {
                    'year': substrings[0],
                    'month': substrings[1],
                    'day': substrings[2],
                }
            if len(substrings) == 2:
                data = {'year': substrings[0], 'month': substrings[1]}
            if len(substrings) == 1:
                data = {'year': substrings[0]}

        super().process(formdata, data)


class DateForm(Form):
    @cached_property
    def data(self):
        data = super().data
        try:
            if all(k in data for k in ('day', 'month', 'year')):
                return '{year:04d}-{month:02d}-{day:02d}'.format(
                    year=int(data['year']),
                    month=int(data['month']),
                    day=int(data['day']),
                )

            if all(k in data for k in ('month', 'year')):
                return '{year:04d}-{month:02d}'.format(
                    year=int(data['year']), month=int(data['month'])
                )

            if 'year' in data and data['year']:
                return '{year:04d}'.format(year=int(data['year']))

        except (TypeError, ValueError):
            return None


def get_form(form_type, validate_with):
    class CustomDateForm(DateForm):
        pass

    if form_type in DateFormType:
        # Validation is only ever added to the 1 field that shows in all 3 variants
        # This is to prevent an error message for each input box
        CustomDateForm.year = StringField(validators=validate_with)

    if form_type in [DateFormType.YearMonth, DateFormType.YearMonthDay]:
        CustomDateForm.month = StringField()

    if form_type == DateFormType.YearMonthDay:
        CustomDateForm.day = StringField()

    return CustomDateForm
