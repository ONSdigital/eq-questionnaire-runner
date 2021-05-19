import re
from dataclasses import asdict, dataclass, field
from functools import cached_property
from typing import Any, Dict, Iterable, List, Mapping, Optional, Union

from flask import current_app
from flask import render_template as flask_render_template
from flask import request
from flask import session as cookie_session
from flask import url_for
from flask_babel import get_locale, lazy_gettext

from app.helpers.language_helper import get_languages_context

CENSUS_EN_BASE_URL = "https://census.gov.uk/"
CENSUS_CY_BASE_URL = "https://cyfrifiad.gov.uk/"
CENSUS_NIR_BASE_URL = f"{CENSUS_EN_BASE_URL}ni/"


@dataclass
class Link:
    text: str
    url: str
    target: Optional[str] = "_blank"


@dataclass
class ContextOptions:
    """Valid options for defining context."""

    page_header_logo: Optional[str] = lazy_gettext("ons-logo-pos-en")
    page_header_logo_alt: Optional[str] = lazy_gettext(
        "Office for National Statistics logo"
    )
    copyright_declaration: Optional[str] = lazy_gettext(
        "Crown copyright and database rights 2020 OS 100019153."
    )
    copyright_text: Optional[str] = lazy_gettext(
        "Use of address data is subject to the terms and conditions."
    )
    title_logo: Optional[str] = None
    title_logo_alt: Optional[str] = None
    header_logo: Optional[str] = None
    mobile_logo: Optional[str] = None
    powered_by_logo: Optional[str] = None
    powered_by_logo_alt: Optional[str] = None
    lang: str = "en"
    crest: bool = True
    footer_links: Optional[Iterable[Link]] = None
    footer_legal_links: Optional[Iterable[Link]] = None


class ContextHelper:
    def __init__(
        self,
        theme: str,
        base_url: str,
        context_options: ContextOptions = ContextOptions(),
    ):
        self._base_url = base_url
        self.context_options = context_options or ContextOptions()
        self._theme = theme
        self._sign_out_url = url_for("session.get_sign_out")
        self._account_service_url = cookie_session.get(
            "account_service_url", f"{self._base_url}en/start"
        )
        self._account_service_log_out_url = cookie_session.get(
            "account_service_log_out_url"
        )
        self._cookie_settings_url = current_app.config["COOKIE_SETTINGS_URL"]
        self._cdn_url = (
            f'{current_app.config["CDN_URL"]}{current_app.config["CDN_ASSETS_PATH"]}'
        )
        self._address_lookup_api = current_app.config["ADDRESS_LOOKUP_API_URL"]
        self._google_tag_manager_id = current_app.config.get("EQ_GOOGLE_TAG_MANAGER_ID")
        self._google_tag_manager_auth = current_app.config.get(
            "EQ_GOOGLE_TAG_MANAGER_AUTH"
        )

    @property
    def context(self) -> Dict[str, Any]:
        return {
            "account_service_url": self._account_service_url,
            "account_service_log_out_url": self._account_service_log_out_url,
            "contact_us_url": asdict(
                Link("Contact us", f"{self._base_url}contact-us/")
            ),
            "cookie_settings_url": self._cookie_settings_url,
            "page_header": self.page_header_context,
            "footer": self.footer_context,
            "languages": get_languages_context(),
            "theme": self._map_theme(self._theme),
            "language_code": get_locale().language,
            "schema_theme": self._theme,
            "survey_title": lazy_gettext("Census 2021"),
            "cdn_url": self._cdn_url,
            "address_lookup_api_url": self._address_lookup_api,
            "data_layer": get_data_layer(self._theme),
            "include_csrf_token": (
                request.url_rule and "POST" in request.url_rule.methods
            ),
            "google_tag_manager_id": self._google_tag_manager_id,
            "google_tag_manager_auth": self._google_tag_manager_auth,
        }

    @cached_property
    def page_header_context(self) -> Dict[str, Any]:
        context = {
            "logo": f"{self.context_options.page_header_logo}",
            "logoAlt": f"{self.context_options.page_header_logo_alt}",
        }

        if self.context_options.title_logo:
            context["titleLogo"] = f"{self.context_options.title_logo}"
        if self.context_options.title_logo_alt:
            context["titleLogoAlt"] = f"{self.context_options.title_logo_alt}"
        if self.context_options.header_logo:
            context["customHeaderLogo"] = self.context_options.header_logo
        if self.context_options.mobile_logo:
            context["mobileLogo"] = self.context_options.mobile_logo

        if "census" in self._theme:
            return {"census": context}

        return context

    @cached_property
    def footer_context(self):
        context = {
            "lang": self.context_options.lang,
            "crest": self.context_options.crest,
            "newTabWarning": lazy_gettext("The following links open in a new tab"),
            "copyrightDeclaration": {
                "copyright": self.context_options.copyright_declaration,
                "text": self.context_options.copyright_text,
            },
        }

        if self._footer_warning:
            context["footerWarning"] = self._footer_warning

        if self.context_options.footer_links:
            for footer_link in self.context_options.footer_links:
                footer_link.url = self._base_url + footer_link.url
            context["rows"] = [{"itemsList": self.context_options.footer_links}]

        if self.context_options.footer_legal_links:
            for footer_legal_link in self.context_options.footer_legal_links:
                url = footer_legal_link.url
                footer_legal_link.url = self._base_url + url
            context["legal"] = [{"itemsList": self.context_options.footer_legal_links}]

        if (
            self.context_options.powered_by_logo
            or self.context_options.powered_by_logo_alt
        ):
            context["poweredBy"] = {
                "logo": self.context_options.powered_by_logo,
                "alt": self.context_options.powered_by_logo_alt,
            }

        return context

    @cached_property
    def _footer_warning(self) -> Union[str, None]:
        if request.blueprint == "post_submission":
            return lazy_gettext(
                "Make sure you <a href='{sign_out_url}'>leave this page</a> or close your browser if using a shared device"
            ).format(sign_out_url=self._sign_out_url)

    @staticmethod
    def _map_theme(theme: str) -> str:
        """Maps a survey schema theme to a design system theme

        :param theme: A schema defined theme
        :returns: A design system theme
        """
        if theme and theme not in ["census", "census-nisra"]:
            return "main"
        return "census"


@dataclass
class CymruContextOptions(ContextOptions):
    footer_links: Iterable[Link] = field(
        default_factory=lambda: [
            Link(
                lazy_gettext("Help"),
                "help/sut-i-ateb-y-cwestiynau/help-y-cwestiynau-ar-lein/",
            ),
            Link(lazy_gettext("Contact us"), "cysylltu-a-ni/"),
            Link(lazy_gettext("Languages"), "help/ieithoedd-a-hygyrchedd/ieithoedd/"),
            Link(
                lazy_gettext("BSL and audio videos"),
                "help/ieithoedd-a-hygyrchedd/hygyrchedd/fideos-hygyrch-gyda-bsl/",
            ),
        ]
    )
    footer_legal_links: Iterable[Link] = field(
        default_factory=lambda: [
            Link(lazy_gettext("Cookies"), "cwcis/"),
            Link(lazy_gettext("Accessibility Statement"), "datganiad-hygyrchedd/"),
            Link(
                lazy_gettext("Privacy and data protection"),
                "preifatrwydd-a-diogelu-data/",
            ),
            Link(lazy_gettext("Terms and conditions"), "telerau-ac-amodau/"),
        ]
    )


@dataclass
class CensusContextOptions(ContextOptions):
    title_logo: str = "census-logo-en"
    title_logo_alt: str = lazy_gettext("Census 2021")


@dataclass
class CensusCymruContextOptions(CymruContextOptions):
    title_logo: str = "census-logo-cy"
    title_logo_alt: str = lazy_gettext("Census 2021")


@dataclass
class CensusNISRAContextOptions(CensusContextOptions):
    page_header_logo: str = "nisra-logo-en"
    page_header_logo_alt: str = lazy_gettext(
        "Northern Ireland Statistics and Research Agency logo"
    )
    header_logo: str = "nisra"
    mobile_logo: str = "nisra-logo-en-mobile"
    copyright_declaration: str = lazy_gettext(
        "Crown copyright and database rights 2021 NIMA MOU577.501."
    )
    copyright_text: str = lazy_gettext(
        "Use of address data is subject to the terms and conditions."
    )
    footer_links: Iterable[Link] = field(
        default_factory=lambda: [
            Link(
                lazy_gettext("Help"),
                "help/help-with-the-questions/online-questions-help/",
            ),
            Link(lazy_gettext("Contact us"), "contact-us/"),
        ]
    )
    footer_legal_links: Iterable[Link] = field(
        default_factory=lambda: [
            Link(lazy_gettext("Cookies"), "cookies/"),
            Link(
                lazy_gettext("Accessibility statement"),
                "accessibility-statement/",
            ),
            Link(
                lazy_gettext("Privacy and data protection"),
                "privacy-and-data-protection/",
            ),
            Link(
                lazy_gettext("Terms and conditions"),
                "terms-and-conditions/",
            ),
        ]
    )
    powered_by_logo: str = "nisra-logo-black-en"
    powered_by_logo_alt: str = "NISRA - Northern Ireland Statistics and Research Agency"


def generate_context(
    theme: str,
    base_url: str,
    language: str,
) -> Dict[str, Any]:
    context_options = {
        "business": ContextOptions,
        "health": ContextOptions,
        "social": ContextOptions if language == "en" else CymruContextOptions,
        "census": (
            CensusContextOptions if language == "en" else CensusCymruContextOptions
        ),
        "default": ContextOptions,
        "census-nisra": CensusNISRAContextOptions,
    }

    return ContextHelper(
        theme,
        base_url,
        context_options[theme](),
    ).context


def render_template(template: str, **kwargs: Mapping) -> str:
    theme = cookie_session.get("theme", current_app.config["SURVEY_TYPE"])
    language = get_locale().language
    base_url = get_base_url("theme", language)

    context = generate_context(
        theme,
        base_url,
        language,
    )
    template = f"{template.lower()}.html"
    return flask_render_template(
        template,
        csp_nonce=request.csp_nonce,  # type: ignore
        **context,
        **kwargs,
    )


def get_base_url(schema_theme: str, language_code: str) -> str:
    if language_code == "cy":
        return CENSUS_CY_BASE_URL

    if schema_theme == "census-nisra":
        return CENSUS_NIR_BASE_URL

    return CENSUS_EN_BASE_URL


def get_data_layer(theme: str) -> List:
    if theme == "census-nisra":
        return [{"nisra": True}]

    if theme == "census":
        return [{"nisra": False}]

    return []
