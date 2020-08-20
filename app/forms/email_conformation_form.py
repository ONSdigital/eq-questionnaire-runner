from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Email


class EmailConformationForm(FlaskForm):
    email = StringField(
        "username",
        validators=[
            InputRequired("Enter an email address to continue"),
            Email("format"),
        ],
    )

    def map_errors(self):
        ordered_errors = [("email", self.errors["email"][0])] if self.errors else []
        return ordered_errors
