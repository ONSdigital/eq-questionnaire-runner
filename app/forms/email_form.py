from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Email


class EmailForm(FlaskForm):
    email_address = StringField(
        "username",
        validators=[
            InputRequired("Enter an email address to continue"),
            Email("Enter an email in a valid format, for example name@example.com"),
        ],
    )

    def map_errors(self):
        ordered_errors = []
        for error in self.errors:
            ordered_errors += [(error, self.errors[error][0])]
        return ordered_errors
