from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping, Optional

from flask_babel import lazy_gettext

from app.settings import ACCOUNT_SERVICE_BASE_URL
from app.survey_config.link import Link
from app.survey_config.survey_config import SurveyConfig


@dataclass
class BusinessSurveyConfig(
    SurveyConfig,
):
    base_url: Optional[str] = ACCOUNT_SERVICE_BASE_URL
    account_service_url: str = f"{base_url}/sign-in/logout"
    survey_title: str = "ONS Business Surveys"

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
