from wtforms import TextAreaField


class MaxTextAreaField(TextAreaField):
    def __init__(self, label="", validators=None, rows=None, maxlength=None, **kwargs):
        super(MaxTextAreaField, self).__init__(label, validators, **kwargs)
        self.rows = rows
        self.maxlength = maxlength
