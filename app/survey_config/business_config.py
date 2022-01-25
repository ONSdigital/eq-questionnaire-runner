from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping, Optional
from warnings import warn

from flask_babel import lazy_gettext

from app.survey_config.link import HeaderLink, Link
from app.survey_config.survey_config import SurveyConfig


@dataclass
class BusinessSurveyConfig(
    SurveyConfig,
):
    survey_title: str = "ONS Business Surveys"
    footer_links: Iterable[MutableMapping] = field(default_factory=list)
    footer_legal_links: Iterable[Mapping] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()

        if not self.account_service_log_out_url:
            self.account_service_log_out_url: str = (
                f"{self.stripped_base_url}/sign-in/logout"
            )

        if not self.account_service_my_account_url:
            self.account_service_my_account_url: str = (
                f"{self.stripped_base_url}/my-account"
            )

        if not self.account_service_todo_url:
            self.account_service_todo_url: str = (
                f"{self.stripped_base_url}/surveys/todo"
            )

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
                    lazy_gettext("My account"),
                    self.account_service_my_account_url,
                    id="header-link-my-account",
                ).__dict__,
                HeaderLink(
                    lazy_gettext("Sign out"), sign_out_url, id="header-link-sign-out"
                ).__dict__,
            ]
            if is_authenticated
            else None
        )

    @property
    def stripped_base_url(self) -> str:
        warn(
            "base_url contains extra pathing which will eventually be corrected and this function will need to be removed"
        )
        return self.base_url.replace("/surveys/todo", "")
