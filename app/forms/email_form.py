from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email, InputRequired

from app.forms import error_messages


class EmailForm(FlaskForm):
    email = StringField(
        validators=[
            InputRequired(error_messages["MANDATORY_EMAIL"]),
            Email(error_messages["INVALID_EMAIL_FORMAT"]),
        ],
    )

    def map_errors(self):
        ordered_errors = []
        for error in self.errors:
            ordered_errors += [(error, self.errors[error][0])]
        return ordered_errors

    def validate(self, extra_validators=None):
        super(EmailForm, self).validate(extra_validators)
        valid_fields = FlaskForm.validate(self)
        return valid_fields
