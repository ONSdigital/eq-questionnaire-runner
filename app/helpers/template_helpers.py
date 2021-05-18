import re
from dataclasses import dataclass, asdict
from functools import cached_property, lru_cache
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


@lru_cache
def en_static_content_urls(base_url: str) -> Dict[str, str]:
    help_path = "help/how-to-answer-questions/online-questions-help/"
    cookies_path = "cookies/"
    accessibility_statement_path = "accessibility-statement/"
    privacy_and_data_protection_path = "privacy-and-data-protection/"
    terms_and_conditions_path = "terms-and-conditions/"
    contact_us = "contact-us/"
    languages = "help/languages-and-accessibility/languages/"
    bsl_and_audio_videos = (
        "help/languages-and-accessibility/accessibility/accessible-videos-with-bsl/"
    )

    return {
        "help": f"{base_url}{help_path}",
        "cookies": f"{base_url}{cookies_path}",
        "accessibility_statement": f"{base_url}{accessibility_statement_path}",
        "privacy_and_data_protection": f"{base_url}{privacy_and_data_protection_path}",
        "terms_and_conditions": f"{base_url}{terms_and_conditions_path}",
        "contact_us": f"{base_url}{contact_us}",
        "languages": f"{base_url}{languages}",
        "bsl_and_audio_videos": f"{base_url}{bsl_and_audio_videos}",
    }


@lru_cache
def cy_static_content_urls(base_url: str) -> Dict[str, str]:
    help_path = "help/sut-i-ateb-y-cwestiynau/help-y-cwestiynau-ar-lein/"
    cookies_path = "cwcis/"
    accessibility_statement_path = "datganiad-hygyrchedd/"
    privacy_and_data_protection_path = "preifatrwydd-a-diogelu-data/"
    terms_and_conditions_path = "telerau-ac-amodau/"
    contact_us = "cysylltu-a-ni/"
    languages = "help/ieithoedd-a-hygyrchedd/ieithoedd/"
    bsl_and_audio_videos = (
        "help/ieithoedd-a-hygyrchedd/hygyrchedd/fideos-hygyrch-gyda-bsl/"
    )

    return {
        "help": f"{base_url}{help_path}",
        "cookies": f"{base_url}{cookies_path}",
        "accessibility_statement": f"{base_url}{accessibility_statement_path}",
        "privacy_and_data_protection": f"{base_url}{privacy_and_data_protection_path}",
        "terms_and_conditions": f"{base_url}{terms_and_conditions_path}",
        "contact_us": f"{base_url}{contact_us}",
        "languages": f"{base_url}{languages}",
        "bsl_and_audio_videos": f"{base_url}{bsl_and_audio_videos}",
    }


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
    footer_links: Optional[Iterable[Mapping]] = None
    footer_legal_links: Optional[Iterable[Mapping]] = None
    footer_warning: Optional[str] = None


@dataclass
class Context:
    """The context used to render a flask template."""

    account_service_url: str
    account_service_log_out_url: str
    contact_us_url: str
    cookie_settings_url: str
    page_header: Mapping
    footer: Mapping
    languages: Mapping
    theme: str
    language_code: str
    schema_theme: str
    survey_title: str
    cdn_url: str
    csp_nonce: str
    address_lookup_api_url: str
    data_layer: Iterable
    include_csrf_token: bool
    sign_out_url: str
    google_tag_manager_id: str
    google_tag_manager_auth: str


class ContextHelper:
    def __init__(self, base_url: str):
        self._base_url = base_url

    def context(self) -> str:
        theme = cookie_session.get("theme", current_app.config["SURVEY_TYPE"])
        sign_out_url = url_for("session.get_sign_out")

        return Context(
            account_service_url=cookie_session.get(
                "account_service_url", f"{CENSUS_EN_BASE_URL}en/start"
            ),
            account_service_log_out_url=cookie_session.get(
                "account_service_log_out_url"
            ),
            contact_us_url=self.static_content_urls["contact_us"],
            cookie_settings_url=current_app.config["COOKIE_SETTINGS_URL"],
            page_header=self.page_header_context,
            footer=self.footer_context(
                sign_out_url,
            ),
            languages=get_languages_context(),
            theme=_map_theme(theme),
            language_code=get_locale().language,
            schema_theme=theme,
            survey_title=lazy_gettext("Census 2021"),
            cdn_url=f'{current_app.config["CDN_URL"]}{current_app.config["CDN_ASSETS_PATH"]}',
            csp_nonce=request.csp_nonce,
            address_lookup_api_url=current_app.config["ADDRESS_LOOKUP_API_URL"],
            data_layer=get_data_layer(theme),
            include_csrf_token=request.url_rule and "POST" in request.url_rule.methods,
            sign_out_url=url_for("session.get_sign_out"),
            google_tag_manager_id=current_app.config.get("EQ_GOOGLE_TAG_MANAGER_ID"),
            google_tag_manager_auth=current_app.config.get(
                "EQ_GOOGLE_TAG_MANAGER_AUTH"
            ),
        )

    @cached_property
    def static_content_urls(self):
        return en_static_content_urls(self._base_url)

    @cached_property
    def page_header_context(self) -> Dict[str, Any]:
        return self._page_header_context(ContextOptions())

    def _page_header_context(self, context_options: ContextOptions):
        context = {
            "logo": f"{context_options.page_header_logo}",
            "logoAlt": f"{context_options.page_header_logo_alt}",
        }

        if context_options.title_logo:
            context["titleLogo"] = f"{context_options.title_logo}"
        if context_options.title_logo_alt:
            context["titleLogoAlt"] = f"{context_options.title_logo_alt}"
        if context_options.header_logo:
            context["customHeaderLogo"] = context_options.header_logo
        if context_options.mobile_logo:
            context["mobileLogo"] = context_options.mobile_logo

        return context

    @staticmethod
    def _footer_warning(sign_out_url: Optional[str]) -> Union[str, None]:
        if request.blueprint == "post_submission":
            return lazy_gettext(
                "Make sure you <a href='{sign_out_url}'>leave this page</a> or close your browser if using a shared device"
            ).format(sign_out_url=sign_out_url)

    def footer_context(self, sign_out_url: Optional[str] = None) -> Dict[str, Any]:
        return self._footer_context(
            ContextOptions(footer_warning=self._footer_warning(sign_out_url))
        )

    @staticmethod
    def _footer_context(context_options: ContextOptions):
        context = {
            "lang": context_options.lang,
            "crest": context_options.crest,
            "newTabWarning": lazy_gettext("The following links open in a new tab"),
            "copyrightDeclaration": {
                "copyright": context_options.copyright_declaration,
                "text": context_options.copyright_text,
            },
        }

        if context_options.footer_links:
            context["rows"] = [{"itemsList": context_options.footer_links}]
        if context_options.footer_legal_links:
            context["legal"] = [{"itemsList": context_options.footer_legal_links}]
        if context_options.footer_warning:
            context["footerWarning"] = context_options.footer_warning
        if context_options.powered_by_logo or context_options.powered_by_logo_alt:
            context["poweredBy"] = {
                "logo": context_options.powered_by_logo,
                "alt": context_options.powered_by_logo_alt,
            }

        return context


class CymruContextHelper(ContextHelper):
    @cached_property
    def static_content_urls(self):
        return cy_static_content_urls(self._base_url)


class CensusContextHelper(ContextHelper):
    @cached_property
    def page_header_context(self) -> Dict[str, Any]:
        context_options = ContextOptions(
            title_logo="census-logo-en",
            title_logo_alt=lazy_gettext("Census 2021"),
        )
        return {"census": self._page_header_context(context_options)}


class CensusCymruContextHelper(CensusContextHelper):
    @cached_property
    def static_content_urls(self):
        return cy_static_content_urls(self._base_url)

    @cached_property
    def page_header_context(self) -> Dict[str, Any]:
        context_options = ContextOptions(
            title_logo="census-logo-cy",
            title_logo_alt=lazy_gettext("Census 2021"),
        )
        return {"census": self._page_header_context(context_options)}


class CensusNISRAContextHelper(ContextHelper):
    @cached_property
    def static_content_urls(self) -> Dict[str, str]:
        help_path = "help/help-with-the-questions/online-questions-help/"
        cookies_path = "cookies/"
        accessibility_statement_path = "accessibility-statement/"
        privacy_and_data_protection_path = "privacy-and-data-protection/"
        terms_and_conditions_path = "terms-and-conditions/"
        contact_us = "contact-us/"

        return {
            "help": f"{self._base_url}{help_path}",
            "cookies": f"{self._base_url}{cookies_path}",
            "accessibility_statement": f"{self._base_url}{accessibility_statement_path}",
            "privacy_and_data_protection": f"{self._base_url}{privacy_and_data_protection_path}",
            "terms_and_conditions": f"{self._base_url}{terms_and_conditions_path}",
            "contact_us": f"{self._base_url}{contact_us}",
        }

    @cached_property
    def legal_links(self):
        return [
            {
                "text": lazy_gettext("Cookies"),
                "url": self.static_content_urls["cookies"],
                "target": "_blank",
            },
            {
                "text": lazy_gettext("Accessibility statement"),
                "url": self.static_content_urls["accessibility_statement"],
                "target": "_blank",
            },
            {
                "text": lazy_gettext("Privacy and data protection"),
                "url": self.static_content_urls["privacy_and_data_protection"],
                "target": "_blank",
            },
            {
                "text": lazy_gettext("Terms and conditions"),
                "url": self.static_content_urls["terms_and_conditions"],
                "target": "_blank",
            },
        ]

    @cached_property
    def page_header_context(self) -> Dict[str, str]:
        context_options = ContextOptions(
            page_header_logo="nisra-logo-en",
            page_header_logo_alt=lazy_gettext(
                "Northern Ireland Statistics and Research Agency logo"
            ),
            title_logo="census-logo-en",
            title_logo_alt="Census 2021",
            header_logo="nisra",
            mobile_logo="nisra-logo-en-mobile",
        )

        return self._page_header_context(context_options)

    def footer_context(self, sign_out_url: Optional[str] = None) -> Dict[str, Any]:
        return self._footer_context(
            ContextOptions(
                copyright_declaration=lazy_gettext(
                    "Crown copyright and database rights 2021 NIMA MOU577.501."
                ),
                copyright_text=lazy_gettext(
                    "Use of address data is subject to the terms and conditions."
                ),
                footer_warning=self._footer_warning(sign_out_url),
                footer_links=self.footer_links,
                footer_legal_links=self.legal_links,
                powered_by_logo="nisra-logo-black-en",
                powered_by_logo_alt="NISRA - Northern Ireland Statistics and Research Agency",
            )
        )

    @cached_property
    def footer_links(self) -> List[Dict[str, Any]]:
        return [
            {
                "text": lazy_gettext("Help"),
                "url": self.static_content_urls["help"],
                "target": "_blank",
            },
            {
                "text": lazy_gettext("Contact us"),
                "url": self.static_content_urls["contact_us"],
                "target": "_blank",
            },
        ]


def context_helper_factory(
    theme: str, language: str, base_url: str
) -> Union[ContextHelper, CensusContextHelper, CensusNISRAContextHelper]:
    context_helpers = {
        "business": ContextHelper,
        "health": ContextHelper,
        "social": ContextHelper if language == "en" else CymruContextHelper,
        "census": CensusContextHelper if language == "en" else CensusCymruContextHelper,
        "default": CensusContextHelper,
        "census-nisra": CensusNISRAContextHelper,
    }

    return context_helpers[theme](base_url)


def _map_theme(theme: str) -> str:
    """Maps a survey schema theme to a design system theme

    :param theme: A schema defined theme
    :returns: A design system theme
    """
    if theme and theme not in ["census", "census-nisra"]:
        return "main"
    return "census"


def render_template(template: str, **kwargs: Mapping) -> str:
    language = get_locale().language
    theme = cookie_session.get("theme", current_app.config["SURVEY_TYPE"])
    base_url = get_base_url(theme, language)
    context = context_helper_factory(theme, language, base_url).context()
    template = f"{template.lower()}.html"
    return flask_render_template(
        template,
        **asdict(context),
        **kwargs,
    )


def get_base_url(schema_theme: str, language_code: str) -> str:
    if language_code == "cy":
        return CENSUS_CY_BASE_URL

    if schema_theme == "census-nisra":
        return CENSUS_NIR_BASE_URL

    return CENSUS_EN_BASE_URL


def safe_content(content: str) -> str:
    """Make content safe.

    Replaces variable with ellipsis and strips any HTML tags.

    :param (str) content: Input string.
    :returns (str): Modified string.
    """
    if content is not None:
        # Replace piping with ellipsis
        content = re.sub(r"{.*?}", "…", content)
        # Strip HTML Tags
        content = re.sub(r"</?[^>]+>", "", content)
    return content


def get_data_layer(theme: str) -> List:
    if theme == "census-nisra":
        return [{"nisra": True}]

    if theme == "census":
        return [{"nisra": False}]

    return []
