from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping, Optional
from urllib.parse import urlencode
from warnings import warn

from flask_babel import lazy_gettext

from app.helpers.metadata_helpers import get_ru_ref_without_check_letter
from app.settings import read_file
from app.survey_config.link import HeaderLink, Link
from app.survey_config.survey_config import SurveyConfig


@dataclass
class BusinessSurveyConfig(SurveyConfig):
    survey_title: str = "ONS Business Surveys"
    footer_links: Iterable[MutableMapping] = field(default_factory=list)
    footer_legal_links: Iterable[Mapping] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.base_url = self._stripped_base_url
        super().__post_init__()

        if not self.account_service_log_out_url:
            self.account_service_log_out_url: str = f"{self.base_url}/sign-in/logout"

        if not self.account_service_my_account_url:
            self.account_service_my_account_url: str = f"{self.base_url}/my-account"

        if not self.account_service_todo_url:
            self.account_service_todo_url: str = f"{self.base_url}/surveys/todo"

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
                "ru_ref": get_ru_ref_without_check_letter(ru_ref),
            }
            return f"{self.base_url}/surveys/surveys-help?{urlencode(request_data)}"

        return f"{self.base_url}/help"

    def get_service_links(
        self,
        sign_out_url: str,
        *,
        is_authenticated: bool,
        cookie_has_theme: bool,
        ru_ref: Optional[str],
    ) -> Optional[list[dict]]:
        links = (
            [
                HeaderLink(
                    lazy_gettext("Help"),
                    self._get_account_service_help_url(
                        is_authenticated=is_authenticated, ru_ref=ru_ref
                    ),
                    id="header-link-help",
                ).__dict__
            ]
            if cookie_has_theme
            else []
        )
        if is_authenticated:
            links.extend(
                [
                    HeaderLink(
                        lazy_gettext("My account"),
                        self.account_service_my_account_url,
                        id="header-link-my-account",
                    ).__dict__,
                    HeaderLink(
                        lazy_gettext("Sign out"),
                        sign_out_url,
                        id="header-link-sign-out",
                    ).__dict__,
                ]
            )

        return links

    def get_footer_links(self, cookie_has_theme: bool) -> list[dict]:
        links = [Link(lazy_gettext("What we do"), self.what_we_do_url).as_dict()]

        if cookie_has_theme:
            links.append(
                Link(lazy_gettext("Contact us"), self.contact_us_url).as_dict()
            )

        links.append(
            Link(
                lazy_gettext("Accessibility"),
                self.accessibility_url,
            ).as_dict()
        )

        return links

    def get_footer_legal_links(self, cookie_has_theme: bool) -> Optional[list[dict]]:
        if cookie_has_theme:
            return [
                Link(lazy_gettext("Cookies"), self.cookie_settings_url).as_dict(),
                Link(
                    lazy_gettext("Privacy and data protection"),
                    self.privacy_and_data_protection_url,
                ).as_dict(),
            ]

        return None

    @property
    def _stripped_base_url(self) -> str:
        warn(
            "base_url contains extra pathing which will eventually be corrected and this function will need to be removed"
        )
        return self.base_url.replace("/surveys/todo", "")


@dataclass
class NIBusinessSurveyConfig(BusinessSurveyConfig):
    masthead_logo: str = read_file("./templates/assets/images/finance-ni-logo.svg")
    masthead_logo_mobile: str = read_file(
        "./templates/assets/images/finance-ni-mobile-logo.svg"
    )


@dataclass
class DBTDSITBusinessSurveyConfig(BusinessSurveyConfig):
    masthead_logo: str = read_file(
        "./templates/assets/images/dbt-logo-stacked.svg"
    ) + read_file("./templates/assets/images/dsit-logo-stacked.svg")


@dataclass
class DBTDSITNIBusinessSurveyConfig(BusinessSurveyConfig):
    masthead_logo: str = (
        read_file("./templates/assets/images/dbt-logo-stacked.svg")
        + read_file("./templates/assets/images/dsit-logo-stacked.svg")
        + read_file("./templates/assets/images/finance-ni-logo-stacked.svg")
    )


@dataclass
class DBTBusinessSurveyConfig(BusinessSurveyConfig):
    masthead_logo: str = read_file("./templates/assets/images/dbt-logo-stacked.svg")


@dataclass
class DBTNIBusinessSurveyConfig(BusinessSurveyConfig):
    masthead_logo: str = read_file(
        "./templates/assets/images/dbt-logo-stacked.svg"
    ) + read_file("./templates/assets/images/finance-ni-logo-stacked.svg")


@dataclass
class DESNZBusinessSurveyConfig(BusinessSurveyConfig):
    masthead_logo: str = read_file("./templates/assets/images/desnz-logo-stacked.svg")


@dataclass
class DESNZNIBusinessSurveyConfig(BusinessSurveyConfig):
    masthead_logo: str = read_file(
        "./templates/assets/images/desnz-logo-stacked.svg"
    ) + read_file("./templates/assets/images/finance-ni-logo-stacked.svg")


@dataclass
class ORRBusinessSurveyConfig(BusinessSurveyConfig):
    masthead_logo: str = read_file("./templates/assets/images/orr-logo.svg")
    masthead_logo_mobile: str = read_file(
        "./templates/assets/images/orr-mobile-logo.svg"
    )
