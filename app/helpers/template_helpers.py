from dataclasses import dataclass, field
from functools import cached_property, lru_cache
from typing import Any, Iterable, Mapping, MutableMapping, Optional, Union

from flask import current_app
from flask import render_template as flask_render_template
from flask import request
from flask import session as cookie_session
from flask import url_for
from flask_babel import get_locale, lazy_gettext
from flask_babel.speaklater import LazyString

from app.helpers.language_helper import get_languages_context

DEFAULT_EN_BASE_URL = "https://ons.gov.uk"
CENSUS_EN_BASE_URL = "https://census.gov.uk"
CENSUS_CY_BASE_URL = "https://cyfrifiad.gov.uk"
CENSUS_NIR_BASE_URL = f"{CENSUS_EN_BASE_URL}/ni"


@dataclass
class Link:
    text: LazyString
    url: str
    target: Optional[str] = "_blank"


@dataclass
class SurveyConfig:
    """Valid options for defining survey-based configuration."""

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


class ContextHelper:
    def __init__(
        self,
        language: str,
        is_post_submission: bool,
        include_csrf_token: bool,
        survey_config: SurveyConfig = SurveyConfig(),
    ) -> None:
        self._language = language
        self._is_post_submission = is_post_submission
        self._include_csrf_token = include_csrf_token
        self._survey_config = survey_config
        self._survey_title = cookie_session.get(
            "survey_title", self._survey_config.survey_title
        )
        self._sign_out_url = url_for("session.get_sign_out")
        self._account_service_url = cookie_session.get(
            "account_service_url", self._survey_config.account_service_url
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
                lazy_gettext("Contact us"),
                f"{self._survey_config.base_url}/contact-us/",
            ).__dict__,
            "cookie_settings_url": self._cookie_settings_url,
            "page_header": self.page_header_context,
            "footer": self.footer_context,
            "languages": get_languages_context(self._language),
            "theme": self._survey_config.design_system_theme,
            "language_code": self._language,
            "survey_title": self._survey_title,
            "cdn_url": self._cdn_url,
            "address_lookup_api_url": self._address_lookup_api,
            "data_layer": self._survey_config.data_layer,
            "include_csrf_token": self._include_csrf_token,
            "google_tag_manager_id": self._google_tag_manager_id,
            "google_tag_manager_auth": self._google_tag_manager_auth,
        }

    @property
    def page_header_context(self) -> dict[str, str]:
        context = {
            "logo": f"{self._survey_config.page_header_logo}",
            "logoAlt": f"{self._survey_config.page_header_logo_alt}",
        }

        if self._survey_title:
            context["title"] = self._survey_title
        if self._survey_config.title_logo:
            context["titleLogo"] = f"{self._survey_config.title_logo}"
        if self._survey_config.title_logo_alt:
            context["titleLogoAlt"] = f"{self._survey_config.title_logo_alt}"
        if self._survey_config.header_logo:
            context["customHeaderLogo"] = self._survey_config.header_logo
        if self._survey_config.mobile_logo:
            context["mobileLogo"] = self._survey_config.mobile_logo

        return context

    @property
    def footer_context(self) -> dict[str, Any]:
        context = {
            "lang": self._language,
            "crest": self._survey_config.crest,
            "newTabWarning": lazy_gettext("The following links open in a new tab"),
            "copyrightDeclaration": {
                "copyright": self._survey_config.copyright_declaration,
                "text": self._survey_config.copyright_text,
            },
        }

        if self._footer_warning:
            context["footerWarning"] = self._footer_warning

        if self._survey_config.footer_links:
            context["rows"] = [{"itemsList": self._survey_config.footer_links}]

        if self._survey_config.footer_legal_links:
            context["legal"] = [{"itemsList": self._survey_config.footer_legal_links}]

        if (
            self._survey_config.powered_by_logo
            or self._survey_config.powered_by_logo_alt
        ):
            context["poweredBy"] = {
                "logo": self._survey_config.powered_by_logo,
                "alt": self._survey_config.powered_by_logo_alt,
            }

        return context

    @cached_property
    def _footer_warning(self) -> Optional[str]:
        if self._is_post_submission:
            footer_warning: str = lazy_gettext(
                "Make sure you <a href='{sign_out_url}'>leave this page</a> or close your browser if using a shared device"
            ).format(sign_out_url=self._sign_out_url)

            return footer_warning


@dataclass
class CensusSurveyConfig(
    SurveyConfig,
):
    title_logo: str = "census-logo-en"
    title_logo_alt: LazyString = lazy_gettext("Census 2021")
    base_url: str = CENSUS_EN_BASE_URL
    account_service_url: str = f"{base_url}/en/start"
    design_system_theme: str = "census"
    footer_links: Iterable[MutableMapping] = field(
        default_factory=lambda: [
            Link(
                lazy_gettext("Help"),
                f"{CENSUS_EN_BASE_URL}/help/how-to-answer-questions/online-questions-help/",
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
    survey_title: LazyString = lazy_gettext("Census 2021")


@dataclass
class WelshCensusSurveyConfig(
    CensusSurveyConfig,
):
    title_logo: str = "census-logo-cy"
    base_url: str = CENSUS_CY_BASE_URL
    account_service_url: str = f"{CENSUS_CY_BASE_URL}/en/start"
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
                lazy_gettext("Accessibility statement"),
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
class CensusNISRASurveyConfig(
    CensusSurveyConfig,
):
    base_url: str = CENSUS_NIR_BASE_URL
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
    account_service_url: str = CENSUS_NIR_BASE_URL
    data_layer: Iterable[Mapping] = field(
        default_factory=lambda: [{"nisra": True}], compare=False
    )


@lru_cache
def survey_config_mapping(theme: str, language: str) -> SurveyConfig:
    return {
        "default": SurveyConfig,
        "business": SurveyConfig,
        "health": SurveyConfig,
        "social": SurveyConfig,
        "northernireland": SurveyConfig,
        "census": (WelshCensusSurveyConfig if language == "cy" else CensusSurveyConfig),
        "census-nisra": CensusNISRASurveyConfig,
    }[theme]()


def get_survey_config(
    theme: Optional[str] = None, language: Optional[str] = None
) -> SurveyConfig:
    # The fallback to assigning SURVEY_TYPE to theme is only being added until
    # business feedback on the differentiation between theme and SURVEY_TYPE.
    if not language:
        language = get_locale().language
    if not theme:
        theme = cookie_session.get("theme", current_app.config["SURVEY_TYPE"])

    return survey_config_mapping(theme, language)


def render_template(template: str, **kwargs: Union[str, Mapping]) -> str:
    language = get_locale().language
    survey_config = get_survey_config(language=language)
    is_post_submission = request.blueprint == "post_submission"
    include_csrf_token = bool(request.url_rule and "POST" in request.url_rule.methods)

    context = ContextHelper(
        language, is_post_submission, include_csrf_token, survey_config
    ).context

    template = f"{template.lower()}.html"
    return flask_render_template(
        template,
        csp_nonce=request.csp_nonce,  # type: ignore
        **context,
        **kwargs,
    )
