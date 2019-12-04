import logging

from enum import Enum

from wtforms import Form, StringField, FormField

logger = logging.getLogger(__name__)


class DateFormType(Enum):
    YearMonthDay = {'date_format': 'yyyy-mm-dd'}
    YearMonth = {'date_format': 'yyyy-mm'}
    Year = {'date_format': 'yyyy'}


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


class CachedProperty:
    """ A property that is only computed once per instance and then replaces
        itself with an ordinary attribute. Deleting the attribute resets the
        property.

        Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
        """

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class DateForm(Form):
    @CachedProperty
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
