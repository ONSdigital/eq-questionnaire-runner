from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping

from flask_babel import lazy_gettext

from app.settings import ACCOUNT_SERVICE_BASE_URL
from app.survey_config.link import Link
from app.survey_config.survey_config import SurveyConfig

base_url: str = ACCOUNT_SERVICE_BASE_URL


@dataclass
class BusinessSurveyConfig(
    SurveyConfig,
):

    account_service_surveys_path: str = "/surveys/todo"
    survey_title: str = "ONS Business Surveys"

    footer_links: Iterable[MutableMapping] = field(
        default_factory=lambda: [
            Link(lazy_gettext("What we do"), "#").__dict__,
            Link(
                lazy_gettext("Contact us"),
                f"{base_url}/contact-us/",
            ).__dict__,
            Link(
                lazy_gettext("Accessibility"),
                "#",
            ).__dict__,
        ],
        compare=False,
        hash=False,
    )

    footer_legal_links: Iterable[Mapping] = field(
        default_factory=lambda: [
            Link(lazy_gettext("Cookies"), f"{base_url}/cookies").__dict__,
            Link(
                lazy_gettext("Privacy and data protection"),
                f"{base_url}/privacy-and-data-protection",
            ).__dict__,
        ],
        compare=False,
    )

    def __post_init__(self):
        if not self.account_service_url:
            self.account_service_url: str = f"{self.base_url}/sign-in/logout"
