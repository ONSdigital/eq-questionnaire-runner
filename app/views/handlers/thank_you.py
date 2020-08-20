from flask import session as cookie_session
from werkzeug.exceptions import NotFound
from app.views.contexts.thank_you_context import (
    build_default_thank_you_context,
    build_census_thank_you_context,
)
from app.globals import get_session_store
from app.forms.email_conformation_form import EmailConformationForm
from app.questionnaire.location import InvalidLocationException

class ThankYou:
    DEFAULT_THANK_YOU_TEMPLATE = "thank-you"
    CENSUS_THANK_YOU_TEMPLATE = "census-thank-you"

    CENSUS_TYPE_MAPPINGS = {
        "household": "HH",
        "communal_establishment": "CE",
        "individual": "IR",
    }

    def __init__(self, schema):
        self.session_data = get_session_store().session_data
        self._schema = schema
        if not self.session_data.submitted_time:
            raise NotFound

        self._is_census_theme = cookie_session.get("theme") in [
            "census",
            "census-nisra",
        ]
        self.template = (
            self.CENSUS_THANK_YOU_TEMPLATE
            if self._is_census_theme
            else self.DEFAULT_THANK_YOU_TEMPLATE
        )
        self.email_confirmation = (
            EmailConformationForm()
            if self._schema.get_submission().get("email_confirmation")
            else None
        )

    def get_context(self):

        if not self._is_census_theme:
            return build_default_thank_you_context(self.session_data)

        census_type_code = None
        for census_type in self.CENSUS_TYPE_MAPPINGS:
            if census_type in self.session_data.schema_name:
                census_type_code = self.CENSUS_TYPE_MAPPINGS[census_type]
                break

        return build_census_thank_you_context(
            self.session_data.display_address, census_type_code, self.email_confirmation
        )

    def is_valid_post(self):
        if not self.email_confirmation:
            raise InvalidLocationException
