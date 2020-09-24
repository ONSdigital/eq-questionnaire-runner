from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email, InputRequired

from app.forms import error_messages
from app.forms.questionnaire_form import map_subfield_errors
from app.forms.validators import EmailConfirmationLimitExceededCheck


class EmailForm(FlaskForm):
    email = StringField(
        validators=[
            InputRequired(error_messages["MANDATORY_EMAIL"]),
            Email(error_messages["INVALID_EMAIL_FORMAT"]),
            EmailConfirmationLimitExceededCheck()
        ],
    )

    def map_errors(self):
        return (
            map_subfield_errors(self.errors, self.email.id)
            if self.email.id in self.errors
            else []
        )
