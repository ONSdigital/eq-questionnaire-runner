from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping, Optional
from urllib.parse import urlencode

from flask_babel import lazy_gettext

from app.survey_config.link import HeaderLink, Link
from app.survey_config.survey_config import SurveyConfig


@dataclass
class SocialSurveyConfig(
    SurveyConfig,
):
    survey_title: str = "ONS Social Surveys"
    footer_links: Iterable[MutableMapping] = field(default_factory=list)
    footer_legal_links: Iterable[Mapping] = field(default_factory=list)

    def __post_init__(self):
        self.base_url: str = "https://rh.ons.gov.uk"
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

    def _get_account_service_help_url(
        self, *, is_authenticated: bool, ru_ref: Optional[str]
    ) -> str:
        if self.schema and is_authenticated and ru_ref:
            request_data = {
                "survey_ref": self.schema.json["survey_id"],
                # This is a temporary fix to send upstream only the first 11 characters of the ru_ref.
                # The ru_ref currently is concatenated with the check letter. Which upstream currently do not support.
                # The first 11 characters represents the reporting unit reference.
                # The 12th character is the check letter identifier.
                "ru_ref": ru_ref[:11],
            }
            return f"{self.base_url}/surveys/surveys-help?{urlencode(request_data)}"

        return f"{self.base_url}/help"

    def get_service_links(
        self, sign_out_url: str, *, is_authenticated: bool, ru_ref: Optional[str]
    ) -> Optional[list[dict]]:
        return [
            HeaderLink(
                lazy_gettext("Help"),
                self._get_account_service_help_url(
                    is_authenticated=is_authenticated, ru_ref=ru_ref
                ),
                id="header-link-help",
            ).__dict__
        ]
