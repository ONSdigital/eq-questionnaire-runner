from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping, Optional
from warnings import warn

from flask_babel import lazy_gettext
from flask_login import current_user

from app.globals import get_metadata
from app.settings import RAS_URL
from app.survey_config.link import HeaderLink, Link
from app.survey_config.survey_config import SurveyConfig


@dataclass
class BusinessSurveyConfig(
    SurveyConfig,
):
    survey_title: str = "ONS Business Surveys"
    footer_links: Iterable[MutableMapping] = field(default_factory=list)
    footer_legal_links: Iterable[Mapping] = field(default_factory=list)
    account_service_help_url: str = f"{RAS_URL}/help"

    def __post_init__(self):
        self.base_url = self._stripped_base_url
        super().__post_init__()

        if self.schema:
            self.data_layer: list[dict] = [
                {
                    key: self.schema.json[key]
                    for key in ["form_type", "survey_id", "title"]
                    if key in self.schema.json
                }
            ]

            if current_user and current_user.is_authenticated:
                ru_ref = get_metadata(current_user).get("ru_ref")
                survey_id = self.schema.json["survey_id"]
                self.account_service_help_url = f"{RAS_URL}/surveys/surveys-help?survey_ref={survey_id}&ru_ref={ru_ref}"

        if not self.account_service_log_out_url:
            self.account_service_log_out_url: str = f"{self.base_url}/sign-in/logout"

        if not self.account_service_my_account_url:
            self.account_service_my_account_url: str = f"{self.base_url}/my-account"

        if not self.account_service_todo_url:
            self.account_service_todo_url: str = f"{self.base_url}/surveys/todo"

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

    def get_service_links(
        self, sign_out_url: str, *, is_authenticated: bool
    ) -> Optional[list[dict]]:
        return (
            [
                HeaderLink(
                    lazy_gettext("Help"),
                    self.account_service_help_url,
                    id="header-link-help",
                ).__dict__,
                HeaderLink(
                    lazy_gettext("My account"),
                    self.account_service_my_account_url,
                    id="header-link-my-account",
                ).__dict__,
                HeaderLink(
                    lazy_gettext("Sign out"), sign_out_url, id="header-link-sign-out"
                ).__dict__,
            ]
            if is_authenticated
            else [
                HeaderLink(
                    lazy_gettext("Help"),
                    self.account_service_help_url,
                    id="header-link-help",
                ).__dict__
            ]
        )

    @property
    def _stripped_base_url(self) -> str:
        warn(
            "base_url contains extra pathing which will eventually be corrected and this function will need to be removed"
        )
        return self.base_url.replace("/surveys/todo", "")


@dataclass
class NorthernIrelandBusinessSurveyConfig(BusinessSurveyConfig):

    page_header_logo: str = "ni-finance-logo"
    page_header_logo_alt: str = lazy_gettext(
        "Northern Ireland Department of Finance logo"
    )
    mobile_logo: str = "ni-finance-logo-mobile"
    custom_header_logo: bool = True
