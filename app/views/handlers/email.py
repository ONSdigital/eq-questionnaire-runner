from app.forms.email_conformation_form import EmailConformationForm
from app.questionnaire.location import InvalidLocationException

class Email:
    def __init__(self, schema):

        if not schema.get_submission().get("email_confirmation"):
            raise InvalidLocationException(
                f"location is not valid"
            )

        self.email_confirmation = EmailConformationForm()


    def get_context(self):

        return {
            "email_confirmation": {
                "mapped_errors": self.email_confirmation.map_errors(),
                "form": self.email_confirmation,
                "errors": self.email_confirmation.errors,
            }
        }
