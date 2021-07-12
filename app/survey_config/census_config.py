from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping

from flask_babel import lazy_gettext
from flask_babel.speaklater import LazyString

from app.survey_config.link import Link
from app.survey_config.survey_config import SurveyConfig

EN_BASE_URL = "https://census.gov.uk"
CY_BASE_URL = "https://cyfrifiad.gov.uk"
NIR_BASE_URL = f"{EN_BASE_URL}/ni"


@dataclass
class CensusSurveyConfig(
    SurveyConfig,
):
    title_logo: str = "census-logo-en"
    title_logo_alt: LazyString = lazy_gettext("Census 2021")
    base_url: str = EN_BASE_URL
    account_service_url: str = f"{base_url}/en/start"
    design_system_theme: str = "census"
    footer_links: Iterable[MutableMapping] = field(
        default_factory=lambda: [
            Link(
                lazy_gettext("Help"),
                f"{EN_BASE_URL}/help/how-to-answer-questions/online-questions-help/",
            ).__dict__,
            Link(lazy_gettext("Contact us"), f"{EN_BASE_URL}/contact-us/").__dict__,
            Link(
                lazy_gettext("Languages"),
                f"{EN_BASE_URL}/help/languages-and-accessibility/languages/",
            ).__dict__,
            Link(
                lazy_gettext("BSL and audio videos"),
                f"{EN_BASE_URL}/help/languages-and-accessibility/accessibility/accessible-videos-with-bsl/",
            ).__dict__,
        ],
        compare=False,
    )
    footer_legal_links: Iterable[Mapping] = field(
        default_factory=lambda: [
            Link(lazy_gettext("Cookies"), f"{EN_BASE_URL}/cookies/").__dict__,
            Link(
                lazy_gettext("Accessibility statement"),
                f"{EN_BASE_URL}/accessibility-statement/",
            ).__dict__,
            Link(
                lazy_gettext("Privacy and data protection"),
                f"{EN_BASE_URL}/privacy-and-data-protection/",
            ).__dict__,
            Link(
                lazy_gettext("Terms and conditions"),
                f"{EN_BASE_URL}/terms-and-conditions/",
            ).__dict__,
        ],
        compare=False,
    )
    data_layer: Iterable[Mapping] = field(
        default_factory=lambda: [{"nisra": False}], compare=False
    )
    survey_title: LazyString = lazy_gettext("Census 2021")


@dataclass
class WelshCensusSurveyConfig(
    CensusSurveyConfig,
):
    title_logo: str = "census-logo-cy"
    base_url: str = CY_BASE_URL
    account_service_url: str = f"{CY_BASE_URL}/en/start"
    footer_links: Iterable[MutableMapping] = field(
        default_factory=lambda: [
            Link(
                lazy_gettext("Help"),
                f"{CY_BASE_URL}/help/sut-i-ateb-y-cwestiynau/help-y-cwestiynau-ar-lein/",
            ).__dict__,
            Link(lazy_gettext("Contact us"), f"{CY_BASE_URL}/cysylltu-a-ni/").__dict__,
            Link(
                lazy_gettext("Languages"),
                f"{CY_BASE_URL}/help/ieithoedd-a-hygyrchedd/ieithoedd/",
            ).__dict__,
            Link(
                lazy_gettext("BSL and audio videos"),
                f"{CY_BASE_URL}/help/ieithoedd-a-hygyrchedd/hygyrchedd/fideos-hygyrch-gyda-bsl/",
            ).__dict__,
        ],
        compare=False,
        hash=False,
    )
    footer_legal_links: Iterable[Mapping] = field(
        default_factory=lambda: [
            Link(lazy_gettext("Cookies"), f"{CY_BASE_URL}/cwcis/").__dict__,
            Link(
                lazy_gettext("Accessibility statement"),
                f"{CY_BASE_URL}/datganiad-hygyrchedd/",
            ).__dict__,
            Link(
                lazy_gettext("Privacy and data protection"),
                f"{CY_BASE_URL}/preifatrwydd-a-diogelu-data/",
            ).__dict__,
            Link(
                lazy_gettext("Terms and conditions"),
                f"{CY_BASE_URL}/telerau-ac-amodau/",
            ).__dict__,
        ],
        compare=False,
        hash=False,
    )
    data_layer: Iterable[Mapping] = field(
        default_factory=lambda: [{"nisra": False}], compare=False
    )


@dataclass
class CensusNISRASurveyConfig(
    CensusSurveyConfig,
):
    base_url: str = NIR_BASE_URL
    page_header_logo: str = "nisra-logo-en"
    page_header_logo_alt: str = lazy_gettext(
        "Northern Ireland Statistics and Research Agency logo"
    )
    header_logo: str = "nisra"
    mobile_logo: str = "nisra-logo-en-mobile"
    copyright_declaration: LazyString = lazy_gettext(
        "Crown copyright and database rights 2021 NIMA MOU577.501."
    )
    copyright_text: LazyString = lazy_gettext(
        "Use of address data is subject to the terms and conditions."
    )
    footer_links: Iterable[MutableMapping] = field(
        default_factory=lambda: [
            Link(
                lazy_gettext("Help"),
                f"{NIR_BASE_URL}/help/help-with-the-questions/online-questions-help/",
            ).__dict__,
            Link(lazy_gettext("Contact us"), f"{NIR_BASE_URL}/contact-us/").__dict__,
        ],
        compare=False,
        hash=False,
    )
    footer_legal_links: Iterable[Mapping] = field(
        default_factory=lambda: [
            Link(lazy_gettext("Cookies"), f"{NIR_BASE_URL}/cookies/").__dict__,
            Link(
                lazy_gettext("Accessibility statement"),
                f"{NIR_BASE_URL}/accessibility-statement/",
            ).__dict__,
            Link(
                lazy_gettext("Privacy and data protection"),
                f"{NIR_BASE_URL}/privacy-and-data-protection/",
            ).__dict__,
            Link(
                lazy_gettext("Terms and conditions"),
                f"{NIR_BASE_URL}/terms-and-conditions/",
            ).__dict__,
        ],
        compare=False,
        hash=False,
    )
    powered_by_logo: str = "nisra-logo-black-en"
    powered_by_logo_alt: str = "NISRA - Northern Ireland Statistics and Research Agency"
    account_service_url: str = NIR_BASE_URL
    data_layer: Iterable[Mapping] = field(
        default_factory=lambda: [{"nisra": True}], compare=False
    )
