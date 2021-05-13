import re
from functools import cached_property
from typing import Any, Dict, Iterable, List, Mapping, Optional, Union
from dataclasses import dataclass

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
class PageHeaderContextOptions:
    """Valid options for defining page header context."""

    logo: Optional[str] = lazy_gettext("ons-logo-pos-en")
    logo_alt: Optional[str] = lazy_gettext("Office for National Statistics logo")
    title_logo: Optional[str] = None
    title_logo_alt: Optional[str] = None
    custom_header_logo: Optional[str] = None
    mobile_logo: Optional[str] = None


@dataclass
class CopyrightDeclarationOptions:
    """Valid options for defining copyright declarations."""

    copyright: Optional[str] = lazy_gettext(
        "Crown copyright and database rights 2020 OS 100019153."
    )
    text: Optional[str] = lazy_gettext(
        "Use of address data is subject to the terms and conditions."
    )


@dataclass
class PoweredByOptions:
    """Valid options for defining poweredBy context."""

    logo: str
    alt: str


@dataclass
class FooterContextOptions:
    """Valid options for defining footer context."""

    lang: str = "en"
    crest: bool = True
    copyright_declaration: Optional[
        CopyrightDeclarationOptions
    ] = CopyrightDeclarationOptions()
    powered_by: Optional[PoweredByOptions] = None
    rows: Optional[Iterable[Mapping]] = None
    legal: Optional[Iterable[Mapping]] = None
    footer_warning: Optional[str] = None


class ContextHelper:
    def _page_header_context(self, context_options: PageHeaderContextOptions):
        context = {
            "logo": f"{context_options.logo}",
            "logoAlt": f"{context_options.logo_alt}",
        }

        if context_options.title_logo:
            context["titleLogo"] = f"{context_options.title_logo}"
        if context_options.title_logo_alt:
            context["titleLogoAlt"] = f"{context_options.title_logo_alt}"
        if context_options.custom_header_logo:
            context["customHeaderLogo"] = context_options.custom_header_logo
        if context_options.mobile_logo:
            context["mobileLogo"] = context_options.mobile_logo

        return context

    @cached_property
    def page_header_context(self) -> Dict[str, Any]:
        return self._page_header_context(PageHeaderContextOptions())

    @staticmethod
    def _footer_context(context_options: FooterContextOptions):
        context = {
            "lang": context_options.lang,
            "crest": context_options.crest,
            "newTabWarning": lazy_gettext("The following links open in a new tab"),
            "copyrightDeclaration": {
                "copyright": context_options.copyright_declaration.copyright,
                "text": context_options.copyright_declaration.text,
            },
        }
        if context_options.rows:
            context["rows"] = [{"itemsList": context_options.rows}]
        if context_options.legal:
            context["legal"] = [{"itemsList": context_options.legal}]
        if context_options.footer_warning:
            context["footerWarning"] = context_options.footer_warning
        if context_options.powered_by:
            context["poweredBy"] = {
                "logo": context_options.powered_by.logo,
                "alt": context_options.powered_by.alt,
            }

        return context

    @staticmethod
    def _footer_warning(sign_out_url: str) -> Union[str, None]:
        if request.blueprint == "post_submission":
            return lazy_gettext(
                "Make sure you <a href='{sign_out_url}'>leave this page</a> or close your browser if using a shared device"
            ).format(sign_out_url=sign_out_url)

    def footer_context(self, sign_out_url: Optional[str] = None) -> Dict[str, Any]:
        return self._footer_context(
            FooterContextOptions(footer_warning=self._footer_warning(sign_out_url))
        )


class CensusContextHelper(ContextHelper):
    def __init__(self, language: str, base_url: str) -> None:
        self.language = language
        if self.language == "cy":
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
        else:
            help_path = "help/how-to-answer-questions/online-questions-help/"
            cookies_path = "cookies/"
            accessibility_statement_path = "accessibility-statement/"
            privacy_and_data_protection_path = "privacy-and-data-protection/"
            terms_and_conditions_path = "terms-and-conditions/"
            contact_us = "contact-us/"
            languages = "help/languages-and-accessibility/languages/"
            bsl_and_audio_videos = "help/languages-and-accessibility/accessibility/accessible-videos-with-bsl/"

        self.static_content_urls = {
            "help": f"{base_url}{help_path}",
            "cookies": f"{base_url}{cookies_path}",
            "accessibility_statement": f"{base_url}{accessibility_statement_path}",
            "privacy_and_data_protection": f"{base_url}{privacy_and_data_protection_path}",
            "terms_and_conditions": f"{base_url}{terms_and_conditions_path}",
            "contact_us": f"{base_url}{contact_us}",
            "languages": f"{base_url}{languages}",
            "bsl_and_audio_videos": f"{base_url}{bsl_and_audio_videos}",
        }

    @cached_property
    def page_header_context(self) -> Dict[str, Any]:
        context_options = PageHeaderContextOptions(
            title_logo=f"census-logo-{self.language}",
            title_logo_alt=lazy_gettext("Census 2021"),
        )
        return {"census": self._page_header_context(context_options)}

    @cached_property
    def footer_items(self):
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
            {
                "text": lazy_gettext("Languages"),
                "url": self.static_content_urls["languages"],
                "target": "_blank",
            },
            {
                "text": lazy_gettext("BSL and audio videos"),
                "url": self.static_content_urls["bsl_and_audio_videos"],
                "target": "_blank",
            },
        ]


class CensusNISRAContextHelper(ContextHelper):
    def __init__(self, language: str, base_url: str):
        if language == "cy":
            help_path = "help/sut-i-ateb-y-cwestiynau/help-y-cwestiynau-ar-lein/"
            cookies_path = "cwcis/"
            accessibility_statement_path = "datganiad-hygyrchedd/"
            privacy_and_data_protection_path = "preifatrwydd-a-diogelu-data/"
            terms_and_conditions_path = "telerau-ac-amodau/"
            contact_us = "cysylltu-a-ni/"

        else:
            help_path = "help/help-with-the-questions/online-questions-help/"
            cookies_path = "cookies/"
            accessibility_statement_path = "accessibility-statement/"
            privacy_and_data_protection_path = "privacy-and-data-protection/"
            terms_and_conditions_path = "terms-and-conditions/"
            contact_us = "contact-us/"

        self.static_content_urls = {
            "help": f"{base_url}{help_path}",
            "cookies": f"{base_url}{cookies_path}",
            "accessibility_statement": f"{base_url}{accessibility_statement_path}",
            "privacy_and_data_protection": f"{base_url}{privacy_and_data_protection_path}",
            "terms_and_conditions": f"{base_url}{terms_and_conditions_path}",
            "contact_us": f"{base_url}{contact_us}",
        }

    @cached_property
    def legal_items(self):
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
        context_options = PageHeaderContextOptions(
            logo="nisra-logo-en",
            logo_alt=lazy_gettext(
                "Northern Ireland Statistics and Research Agency logo"
            ),
            title_logo="census-logo-en",
            title_logo_alt="Census 2021",
            custom_header_logo="nisra",
            mobile_logo="nisra-logo-en-mobile",
        )

        return self._page_header_context(context_options)

    def footer_context(self, sign_out_url: Optional[str] = None) -> Dict[str, Any]:
        copyright_declaration = CopyrightDeclarationOptions(
            lazy_gettext("Crown copyright and database rights 2021 NIMA MOU577.501."),
            lazy_gettext("Use of address data is subject to the terms and conditions."),
        )
        powered_by = PoweredByOptions(
            "nisra-logo-black-en",
            "NISRA - Northern Ireland Statistics and Research Agency",
        )

        return self._footer_context(
            FooterContextOptions(
                copyright_declaration=copyright_declaration,
                footer_warning=self._footer_warning(sign_out_url),
                powered_by=powered_by,
                rows=self.footer_items,
                legal=self.legal_items,
            )
        )

    @cached_property
    def footer_items(self) -> List[Dict[str, Any]]:
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
        "social": ContextHelper,
        "census": CensusContextHelper,
        "default": CensusContextHelper,
        "census-nisra": CensusNISRAContextHelper,
    }

    return (
        context_helpers[theme](language, base_url)
        if theme in ("census", "census-nisra", "default")
        else context_helpers[theme]()
    )


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
    context_helper = context_helper_factory(theme, language, base_url)
    survey_title = lazy_gettext("Census 2021")
    page_header_context = context_helper.page_header_context
    page_header_context.update({"title": survey_title})
    google_tag_manager_context = get_google_tag_manager_context()
    cdn_url = f'{current_app.config["CDN_URL"]}{current_app.config["CDN_ASSETS_PATH"]}'
    include_csrf_token = request.url_rule and "POST" in request.url_rule.methods
    account_service_url = cookie_session.get(
        "account_service_url", f"{CENSUS_EN_BASE_URL}en/start"
    )
    sign_out_url = url_for("session.get_sign_out")
    footer_context = context_helper.footer_context(
        sign_out_url,
    )

    template = f"{template.lower()}.html"
    return flask_render_template(
        template,
        account_service_url=account_service_url,
        account_service_log_out_url=cookie_session.get("account_service_log_out_url"),
        contact_us_url=context_helper.static_content_urls["contact_us"],
        cookie_settings_url=current_app.config["COOKIE_SETTINGS_URL"],
        page_header=page_header_context,
        footer=footer_context,
        theme=_map_theme(theme),
        languages=get_languages_context(),
        schema_theme=theme,
        language_code=get_locale().language,
        survey_title=survey_title,
        cdn_url=cdn_url,
        csp_nonce=request.csp_nonce,  # type: ignore
        address_lookup_api_url=current_app.config["ADDRESS_LOOKUP_API_URL"],
        data_layer=get_data_layer(theme),
        include_csrf_token=include_csrf_token,
        sign_out_url=sign_out_url,
        **google_tag_manager_context,
        **kwargs,
    )


def get_google_tag_manager_context() -> Mapping:
    if (google_tag_manager_id := current_app.config["EQ_GOOGLE_TAG_MANAGER_ID"]) and (
        google_tag_manager_auth := current_app.config["EQ_GOOGLE_TAG_MANAGER_AUTH"]
    ):
        return {
            "google_tag_manager_id": google_tag_manager_id,
            "google_tag_manager_auth": google_tag_manager_auth,
        }
    return {}


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
