from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping

from flask_babel import lazy_gettext

from app.survey_config.link import Link
from app.survey_config.survey_config import SurveyConfig


@dataclass
class BusinessSurveyConfig(
    SurveyConfig,
):

    account_service_surveys_path: str = "/surveys/todo"
    survey_title: str = "ONS Business Surveys"
    footer_links: Iterable[MutableMapping] = field(default_factory=list)
    footer_legal_links: Iterable[Mapping] = field(default_factory=list)

    def __post_init__(self):
        if not self.account_service_url:
            self.account_service_url = f"{self.base_url}/sign-in/logout"

        self.footer_links = [
            Link(lazy_gettext("What we do"), self.what_we_do_url).__dict__,
            Link(lazy_gettext("Contact us"), self.contact_us_url).__dict__,
            Link(
                lazy_gettext("Accessibility"),
                self.accessibility_url,
            ).__dict__,
        ]
        self.footer_legal_links = [
            Link(lazy_gettext("Cookies"), self.cookie_settings_url).__dict__,
            Link(
                lazy_gettext("Privacy and data protection"),
                self.privacy_and_data_protection_url,
            ).__dict__,
        ]
