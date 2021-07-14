from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping

from flask_babel import lazy_gettext

from app.survey_config.link import Link
from app.survey_config.survey_config import SurveyConfig

BASE_URL = "https://surveys.ons.gov.uk"


@dataclass
class BusinessSurveyConfig(
    SurveyConfig,
):
    base_url: str = BASE_URL
    account_service_url: str = f"{BASE_URL}/surveys/todo"

    footer_links: Iterable[MutableMapping] = field(
        default_factory=lambda: [
            Link(lazy_gettext("What we do"), "#").__dict__,
            Link(lazy_gettext("Contact us"), "#").__dict__,
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
            Link(lazy_gettext("Cookies"), "#").__dict__,
            Link(
                lazy_gettext("Privacy and data protection"),
                "#",
            ).__dict__,
        ],
        compare=False,
    )
