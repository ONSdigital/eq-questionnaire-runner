from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping, Optional, Union

from flask_babel import lazy_gettext
from flask_babel.speaklater import LazyString

DEFAULT_EN_BASE_URL = "https://ons.gov.uk"


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
    base_url: str = DEFAULT_EN_BASE_URL
    account_service_url: Optional[str] = None
    title_logo: Optional[str] = None
    title_logo_alt: Optional[str] = None
    header_logo: Optional[str] = None
    mobile_logo: Optional[str] = None
    powered_by_logo: Optional[str] = None
    powered_by_logo_alt: Optional[str] = None
    crest: bool = True
    footer_links: Optional[Iterable[MutableMapping]] = None
    footer_legal_links: Optional[Iterable[Mapping]] = None
    survey_title: Optional[LazyString] = None
    design_system_theme: Optional[str] = "main"
    data_layer: Iterable[Union[Mapping]] = field(default_factory=list, compare=False)
