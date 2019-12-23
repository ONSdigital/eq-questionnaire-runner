from wtforms import TextAreaField


class MaxTextAreaField(TextAreaField):
    def __init__(self, label="", validators=None, maxlength=10000, **kwargs):
        super(MaxTextAreaField, self).__init__(label, validators, **kwargs)
        self.maxlength = maxlength
