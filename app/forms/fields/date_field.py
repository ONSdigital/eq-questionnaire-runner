import logging

from wtforms import FormField

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
