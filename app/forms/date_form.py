import logging

from werkzeug.utils import cached_property
from wtforms import Form, FormField

logger = logging.getLogger(__name__)


class DateField(FormField):
    def __init__(self, form_class, **kwargs):
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
