from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping, Optional

from flask_babel import lazy_gettext

from app.settings import ACCOUNT_SERVICE_BASE_URL_SOCIAL
from app.survey_config.link import Link
from app.survey_config.survey_config import SurveyConfig


@dataclass
class SocialSurveyConfig(
    SurveyConfig,
):
    base_url: str = ACCOUNT_SERVICE_BASE_URL_SOCIAL
    survey_title: str = "ONS Social Surveys"
    footer_links: Iterable[MutableMapping] = field(default_factory=list)
    footer_legal_links: Iterable[Mapping] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()

        if self.schema:
            self.data_layer: list[dict] = [
                {
                    key: self.schema.json[key]
                    for key in ["survey_id", "title"]
                    if key in self.schema.json
                }
            ]

        if not self.account_service_log_out_url:
            self.account_service_log_out_url: str = f"{self.base_url}/sign-in/logout"

    def get_footer_links(self, cookie_has_theme: bool) -> list[dict]:
        links = [Link(lazy_gettext("What we do"), self.what_we_do_url).__dict__]

        if cookie_has_theme:
            links.append(Link(lazy_gettext("Contact us"), self.contact_us_url).__dict__)

        links.append(
            Link(
                lazy_gettext("Accessibility"),
                self.accessibility_url,
            ).__dict__
        )

        return links

    def get_footer_legal_links(self, cookie_has_theme: bool) -> Optional[list[dict]]:
        if cookie_has_theme:
            return [
                Link(lazy_gettext("Cookies"), self.cookie_settings_url).__dict__,
                Link(
                    lazy_gettext("Privacy and data protection"),
                    self.privacy_and_data_protection_url,
                ).__dict__,
            ]

        return None
