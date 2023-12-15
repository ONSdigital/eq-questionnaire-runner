from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email, InputRequired

from app.forms import error_messages
from app.forms.questionnaire_form import ErrorList, map_subfield_errors
from app.forms.validators import EmailTLDCheck


class EmailForm(FlaskForm):
    email = StringField(
        validators=[
            InputRequired(error_messages["MANDATORY_EMAIL"]),
            EmailTLDCheck(error_messages["INVALID_EMAIL_FORMAT"]),
            Email(error_messages["INVALID_EMAIL_FORMAT"]),
        ],
        filters=[lambda x: x.strip() if x else None],
    )

    def map_errors(self) -> ErrorList:
        return (
            map_subfield_errors(self.errors, self.email.id)
            if self.email.id in self.errors
            else []
        )
