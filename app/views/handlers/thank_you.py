from flask import session as cookie_session
from werkzeug.exceptions import NotFound
from app.views.contexts.thank_you_context import (
    build_default_thank_you_context,
    build_census_thank_you_context,
)
from app.globals import get_session_store

DEFAULT_THANK_YOU_TEMPLATE = "thank-you"
CENSUS_THANK_YOU_TEMPLATE = "census-thank-you"

CENSUS_CODE_TYPE_MAPPINGS = {
    "household": "HH",
    "communal_establishment": "CE",
    "individual": "IR",
}


class ThankYou:
    def __init__(self):
        self.session_data = get_session_store().session_data

        if not self.session_data.submitted_time:
            raise NotFound

        self._cookie_session = cookie_session
        self._is_default_theme = cookie_session.get("theme") == "default"

    def get_context(self):
        if self._is_default_theme:
            return build_default_thank_you_context(self.session_data)

        census_code = None
        for census_code_type in CENSUS_CODE_TYPE_MAPPINGS:
            if census_code_type in self.session_data.schema_name:
                census_code = CENSUS_CODE_TYPE_MAPPINGS[census_code_type]
                break

        return build_census_thank_you_context(
            self._cookie_session.get("display_address"), census_code
        )

    def get_template(self):
        return (
            DEFAULT_THANK_YOU_TEMPLATE
            if self._is_default_theme
            else CENSUS_THANK_YOU_TEMPLATE
        )
