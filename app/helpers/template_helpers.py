from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Iterable, Mapping, MutableMapping, Optional, Text, Union

from flask import current_app
from flask import render_template as flask_render_template
from flask import request
from flask import session as cookie_session
from flask import url_for
from flask_babel import get_locale, lazy_gettext
from flask_babel.speaklater import LazyString

from app.helpers.language_helper import get_languages_context
from app.settings import CENSUS_CY_BASE_URL, CENSUS_EN_BASE_URL, CENSUS_NIR_BASE_URL


@dataclass
class Link:
    text: Union[str, LazyString]
    url: str
    target: Optional[str] = "_blank"


@dataclass
class ContextOptions:
    """Valid options for defining context."""

    page_header_logo: Optional[str] = "ons-logo-pos-en"
    page_header_logo_alt: Optional[LazyString] = lazy_gettext(
        "Office for National Statistics logo"
    )
    copyright_declaration: Optional[LazyString] = lazy_gettext(
        "Crown copyright and database rights 2020 OS 100019153."
    )
    copyright_text: Optional[LazyString] = lazy_gettext(
        "Use of address data is subject to the terms and conditions."
    )
    base_url: str = CENSUS_EN_BASE_URL
    account_service_url: Optional[str] = None
    title_logo: Optional[str] = None
    title_logo_alt: Optional[str] = None
    header_logo: Optional[str] = None
    mobile_logo: Optional[str] = None
    powered_by_logo: Optional[str] = None
    powered_by_logo_alt: Optional[str] = None
    lang: str = "en"
    crest: bool = True
    footer_links: Optional[Iterable[MutableMapping]] = None
    footer_legal_links: Optional[Iterable[Mapping]] = None
    survey_title: Optional[LazyString] = lazy_gettext("Census 2021")
    design_system_theme: Optional[str] = "main"
    data_layer: Iterable[Union[Mapping]] = field(default_factory=list, compare=False)


class ContextHelper:
    def __init__(
        self,
        theme: str,
        language: str,
        is_post_submission: bool,
        include_csrf_token: bool,
        context_options: ContextOptions = ContextOptions(),
    ) -> None:
        self._theme = theme
        self._language = language
        self._is_post_submission = is_post_submission
        self._include_csrf_token = include_csrf_token
        self.context_options = context_options
        self._sign_out_url = url_for("session.get_sign_out")
        self._account_service_url = cookie_session.get(
            "account_service_url", f"{self.context_options.base_url}en/start"
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
    def context(self) -> dict[str, Any]:
        return {
            "account_service_url": self._account_service_url,
            "account_service_log_out_url": self._account_service_log_out_url,
            "contact_us_url": Link(
                "Contact us", f"{self.context_options.base_url}/contact-us/"
            ).__dict__,
            "cookie_settings_url": self._cookie_settings_url,
            "page_header": self.page_header_context,
            "footer": self.footer_context,
            "languages": get_languages_context(self._language),
            "theme": self.context_options.design_system_theme,
            "language_code": self._language,
            "schema_theme": self._theme,
            "survey_title": self.context_options.survey_title,
            "cdn_url": self._cdn_url,
            "address_lookup_api_url": self._address_lookup_api,
            "data_layer": self.context_options.data_layer,
            "include_csrf_token": (
                request.url_rule and "POST" in request.url_rule.methods
            ),
            "google_tag_manager_id": self._google_tag_manager_id,
            "google_tag_manager_auth": self._google_tag_manager_auth,
        }

    @property
    def page_header_context(self) -> dict[str, Any]:
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

        return context

    @property
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
            context["rows"] = [{"itemsList": self.context_options.footer_links}]

        if self.context_options.footer_legal_links:
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
        if self._is_post_submission:
            return lazy_gettext(
                "Make sure you <a href='{sign_out_url}'>leave this page</a> or close your browser if using a shared device"
            ).format(sign_out_url=self._sign_out_url)


@dataclass
class CensusContextOptions(
    ContextOptions,
):
    title_logo: str = "census-logo-en"
    title_logo_alt: LazyString = lazy_gettext("Census 2021")
    base_url: str = CENSUS_EN_BASE_URL
    account_service_url = f"{base_url}/en/start"
    design_system_theme = "census"
    footer_links: Iterable[MutableMapping] = field(
        default_factory=lambda: [
            Link(
                lazy_gettext("Help"),
                f"{CENSUS_EN_BASE_URL}/help/help-with-the-questions/online-questions-help/",
            ).__dict__,
            Link(
                lazy_gettext("Contact us"), f"{CENSUS_EN_BASE_URL}/contact-us/"
            ).__dict__,
            Link(
                lazy_gettext("Languages"),
                f"{CENSUS_EN_BASE_URL}/help/languages-and-accessibility/languages/",
            ).__dict__,
            Link(
                lazy_gettext("BSL and audio videos"),
                f"{CENSUS_EN_BASE_URL}/help/languages-and-accessibility/accessibility/accessible-videos-with-bsl/",
            ).__dict__,
        ],
        compare=False,
    )
    footer_legal_links: Iterable[Mapping] = field(
        default_factory=lambda: [
            Link(lazy_gettext("Cookies"), f"{CENSUS_EN_BASE_URL}/cookies/").__dict__,
            Link(
                lazy_gettext("Accessibility statement"),
                f"{CENSUS_EN_BASE_URL}/accessibility-statement/",
            ).__dict__,
            Link(
                lazy_gettext("Privacy and data protection"),
                f"{CENSUS_EN_BASE_URL}/privacy-and-data-protection/",
            ).__dict__,
            Link(
                lazy_gettext("Terms and conditions"),
                f"{CENSUS_EN_BASE_URL}/terms-and-conditions/",
            ).__dict__,
        ],
        compare=False,
    )
    data_layer: Iterable[Mapping] = field(
        default_factory=lambda: [{"nisra": False}], compare=False
    )


@dataclass
class CensusContextOptionsCymraeg(
    CensusContextOptions,
):
    title_logo: str = "census-logo-cy"
    title_logo_alt: str = lazy_gettext("Census 2021")
    base_url: str = CENSUS_CY_BASE_URL
    account_service_url = f"{CENSUS_CY_BASE_URL}/en/start"
    design_system_theme = "census"
    footer_links: Iterable[MutableMapping] = field(
        default_factory=lambda: [
            Link(
                lazy_gettext("Help"),
                f"{CENSUS_CY_BASE_URL}/help/sut-i-ateb-y-cwestiynau/help-y-cwestiynau-ar-lein/",
            ).__dict__,
            Link(
                lazy_gettext("Contact us"), f"{CENSUS_CY_BASE_URL}/cysylltu-a-ni/"
            ).__dict__,
            Link(
                lazy_gettext("Languages"),
                f"{CENSUS_CY_BASE_URL}/help/ieithoedd-a-hygyrchedd/ieithoedd/",
            ).__dict__,
            Link(
                lazy_gettext("BSL and audio videos"),
                f"{CENSUS_CY_BASE_URL}/help/ieithoedd-a-hygyrchedd/hygyrchedd/fideos-hygyrch-gyda-bsl/",
            ).__dict__,
        ],
        compare=False,
        hash=False,
    )
    footer_legal_links: Iterable[Mapping] = field(
        default_factory=lambda: [
            Link(lazy_gettext("Cookies"), f"{CENSUS_CY_BASE_URL}/cwcis/").__dict__,
            Link(
                lazy_gettext("Accessibility Statement"),
                f"{CENSUS_CY_BASE_URL}/datganiad-hygyrchedd/",
            ).__dict__,
            Link(
                lazy_gettext("Privacy and data protection"),
                f"{CENSUS_CY_BASE_URL}/preifatrwydd-a-diogelu-data/",
            ).__dict__,
            Link(
                lazy_gettext("Terms and conditions"),
                f"{CENSUS_CY_BASE_URL}/telerau-ac-amodau/",
            ).__dict__,
        ],
        compare=False,
        hash=False,
    )
    data_layer: Iterable[Mapping] = field(
        default_factory=lambda: [{"nisra": False}], compare=False
    )


@dataclass
class CensusNISRAContextOptions(
    CensusContextOptions,
):
    base_url: str = CENSUS_NIR_BASE_URL
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
    footer_links: Iterable[MutableMapping] = field(
        default_factory=lambda: [
            Link(
                lazy_gettext("Help"),
                f"{CENSUS_NIR_BASE_URL}/help/help-with-the-questions/online-questions-help/",
            ).__dict__,
            Link(
                lazy_gettext("Contact us"), f"{CENSUS_NIR_BASE_URL}/contact-us/"
            ).__dict__,
        ],
        compare=False,
        hash=False,
    )
    footer_legal_links: Iterable[Mapping] = field(
        default_factory=lambda: [
            Link(lazy_gettext("Cookies"), f"{CENSUS_NIR_BASE_URL}/cookies/").__dict__,
            Link(
                lazy_gettext("Accessibility statement"),
                f"{CENSUS_NIR_BASE_URL}/accessibility-statement/",
            ).__dict__,
            Link(
                lazy_gettext("Privacy and data protection"),
                f"{CENSUS_NIR_BASE_URL}/privacy-and-data-protection/",
            ).__dict__,
            Link(
                lazy_gettext("Terms and conditions"),
                f"{CENSUS_NIR_BASE_URL}/terms-and-conditions/",
            ).__dict__,
        ],
        compare=False,
        hash=False,
    )
    powered_by_logo: str = "nisra-logo-black-en"
    powered_by_logo_alt: str = "NISRA - Northern Ireland Statistics and Research Agency"
    account_service_url = CENSUS_NIR_BASE_URL
    data_layer: Iterable[Mapping] = field(
        default_factory=lambda: [{"nisra": True}], compare=False
    )


def generate_context(
    theme: str,
    language: str,
    is_post_submission: bool,
    include_csrf_token: bool,
) -> dict[str, Any]:
    return ContextHelper(
        theme,
        language,
        is_post_submission,
        include_csrf_token,
        _context_options(theme, language),
    ).context


def _context_options(theme: str, language: str) -> ContextOptions:
    context_options_mapping = {
        "business": ContextOptions,
        "health": ContextOptions,
        "social": ContextOptions,
        "census": (
            CensusContextOptionsCymraeg if language == "cy" else CensusContextOptions
        ),
        "default": ContextOptions,
        "census-nisra": CensusNISRAContextOptions,
    }
    return context_options_mapping[theme]()


def render_template(template: str, **kwargs: Mapping) -> Text:
    # The fallback to assigning SURVEY_TYPE to theme is only being added until
    # business feedback on the differentiation between theme and SURVEY_TYPE.
    theme = cookie_session.get("theme", current_app.config["SURVEY_TYPE"])
    language = get_locale().language
    is_post_submission = request.blueprint == "post_submission"
    include_csrf_token = request.url_rule and "post" in request.url_rule.methods

    context = generate_context(theme, language, is_post_submission, include_csrf_token)

    template = f"{template.lower()}.html"
    return flask_render_template(
        template,
        csp_nonce=request.csp_nonce,  # type: ignore
        **context,
        **kwargs,
    )
