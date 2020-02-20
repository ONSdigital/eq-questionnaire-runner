from wtforms import StringField


class MaxStringField(StringField):
    def __init__(self, label="", validators=None, maxlength=None, **kwargs):
        super(MaxStringField, self).__init__(label, validators, **kwargs)
        self.maxlength = maxlength
