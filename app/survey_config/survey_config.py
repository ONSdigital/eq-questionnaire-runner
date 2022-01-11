from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping, Optional, Union

from flask_babel import lazy_gettext
from flask_babel.speaklater import LazyString

from app.settings import ACCOUNT_SERVICE_BASE_URL, ONS_URL


@dataclass
class SurveyConfig:
    """Valid options for defining survey-based configuration."""

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
    account_service_url: Optional[str] = None
    account_service_surveys_path: Optional[str] = None
    title_logo: Optional[str] = None
    title_logo_alt: Optional[str] = None
    contact_us_url: str = f"{base_url}/contact-us/"
    cookie_settings_url: str = f"{base_url}/cookies/"
    privacy_and_data_protection_url: str = f"{base_url}/privacy-and-data-protection/"
    accessibility_url: str = f"{ONS_URL}/help/accessibility/"
    what_we_do_url: str = f"{ONS_URL}/aboutus/whatwedo/"
    header_logo: Optional[str] = None
    mobile_logo: Optional[str] = None
    powered_by_logo: Optional[str] = None
    powered_by_logo_alt: Optional[str] = None
    crest: bool = True
    footer_links: Optional[Iterable[MutableMapping]] = None
    footer_legal_links: Optional[Iterable[Mapping]] = None
    survey_title: Optional[LazyString] = None
    design_system_theme: Optional[str] = None
    data_layer: Iterable[Union[Mapping]] = field(default_factory=list, compare=False)
