from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Email
from app.forms import error_messages


class EmailForm(FlaskForm):
    email = StringField(
        validators=[
            InputRequired(error_messages["MANDATORY_EMAIL"]),
            Email(error_messages["MANDATORY_EMAIL_FORMAT"]),
        ],
    )

    def map_errors(self):
        return [(error, self.errors[error][0]) for error in self.errors]
