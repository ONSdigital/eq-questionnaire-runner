from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping

from flask_babel import lazy_gettext
from flask_babel.speaklater import LazyString

from app.questionnaire import QuestionnaireSchema
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.settings import ACCOUNT_SERVICE_BASE_URL, ONS_URL


@dataclass
class SurveyConfig:
    """Valid options for defining survey-based configuration."""

    schema: QuestionnaireSchema | None = None
    copyright_declaration: LazyString | None = lazy_gettext(
        "Crown copyright and database rights 2020 OS 100019153."
    )
    copyright_text: LazyString | None = lazy_gettext(
        "Use of address data is subject to the terms and conditions."
    )
    base_url: str = ACCOUNT_SERVICE_BASE_URL
    account_service_my_account_url: str | None = None
    account_service_todo_url: str | None = None
    account_service_log_out_url: str | None = None
    accessibility_url: str = f"{ONS_URL}/help/accessibility/"
    what_we_do_url: str = f"{ONS_URL}/aboutus/whatwedo/"
    masthead_logo: str | None = None
    masthead_logo_mobile: str | None = None
    crest: bool = True
    footer_links: Iterable[MutableMapping] | None = None
    footer_legal_links: Iterable[Mapping] | None = None
    survey_title: LazyString | None = None
    design_system_theme: str | None = None
    sign_out_button_text: str = lazy_gettext("Save and exit survey")
    contact_us_url: str = field(init=False)
    cookie_settings_url: str = field(init=False)
    cookie_domain: str = field(init=False)
    privacy_and_data_protection_url: str = field(init=False)
    language_code: str | None = None

    def __post_init__(self) -> None:
        self.contact_us_url: str = f"{self.base_url}/contact-us/"
        self.cookie_settings_url: str = f"{self.base_url}/cookies/"
        self.cookie_domain: str = self.cookie_settings_url.split("://")[-1].split("/")[
            0
        ]  # get the FQDN of the cookie settings URL
        self.privacy_and_data_protection_url: str = (
            f"{self.base_url}/privacy-and-data-protection/"
        )
        self.language_code: str = self.language_code or DEFAULT_LANGUAGE_CODE

    def get_service_links(  # pylint: disable=unused-argument, no-self-use
        self,
        sign_out_url: str,
        *,
        is_authenticated: bool,
        cookie_has_theme: bool,
        ru_ref: str | None,
    ) -> list[dict] | None:
        return None

    def get_footer_links(  # pylint: disable=unused-argument, no-self-use
        self, cookie_has_theme: bool
    ) -> list[dict] | None:
        return None

    def get_footer_legal_links(  # pylint: disable=unused-argument, no-self-use
        self, cookie_has_theme: bool
    ) -> list[dict] | None:
        return None
