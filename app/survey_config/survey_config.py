from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping, Optional, Union

from flask_babel import lazy_gettext
from flask_babel.speaklater import LazyString
from flask_login import current_user

from app.globals import get_metadata
from app.questionnaire import QuestionnaireSchema
from app.settings import ACCOUNT_SERVICE_BASE_URL, ONS_URL


@dataclass
class SurveyConfig:
    """Valid options for defining survey-based configuration."""

    schema: Optional[QuestionnaireSchema] = None
    page_header_logo: Optional[str] = "ons-logo-en"
    page_header_logo_alt: Optional[LazyString] = lazy_gettext(
        "Office for National Statistics logo"
    )
    copyright_declaration: Optional[LazyString] = lazy_gettext(
        "Crown copyright and database rights 2020 OS 100019153."
    )
    copyright_text: Optional[LazyString] = lazy_gettext(
        "Use of address data is subject to the terms and conditions."
    )
    base_url: str = ACCOUNT_SERVICE_BASE_URL
    account_service_my_account_url: Optional[str] = None
    account_service_todo_url: Optional[str] = None
    account_service_log_out_url: Optional[str] = None
    title_logo: Optional[str] = None
    title_logo_alt: Optional[str] = None
    accessibility_url: str = f"{ONS_URL}/help/accessibility/"
    what_we_do_url: str = f"{ONS_URL}/aboutus/whatwedo/"
    custom_header_logo: bool = False
    mobile_logo: Optional[str] = None
    powered_by_logo: Optional[str] = None
    powered_by_logo_alt: Optional[str] = None
    crest: bool = True
    footer_links: Optional[Iterable[MutableMapping]] = None
    footer_legal_links: Optional[Iterable[Mapping]] = None
    survey_title: Optional[LazyString] = None
    design_system_theme: Optional[str] = None
    data_layer: list[dict[str, Union[str, bool]]] = field(
        default_factory=list, compare=False
    )
    sign_out_button_text: str = lazy_gettext("Save and exit survey")
    contact_us_url: str = field(init=False)
    cookie_settings_url: str = field(init=False)
    privacy_and_data_protection_url: str = field(init=False)

    def __post_init__(self):
        if current_user and get_metadata(current_user):
            if tx_id := get_metadata(current_user).get("tx_id"):
                self.data_layer.append({"tx_id": tx_id})
        self.contact_us_url: str = f"{self.base_url}/contact-us/"
        self.cookie_settings_url: str = f"{self.base_url}/cookies/"
        self.privacy_and_data_protection_url: str = (
            f"{self.base_url}/privacy-and-data-protection/"
        )

    def get_service_links(  # pylint: disable=unused-argument, no-self-use
        self,
        sign_out_url: str,
        *,
        is_authenticated: bool,
        ru_ref: Optional[str],
    ) -> Optional[list[dict]]:
        return None
