import re
from functools import lru_cache
from typing import Any, Dict, List, Mapping, Optional, Union

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
DEFAULT_THEME = "census"


@lru_cache(maxsize=None)
def get_page_header_context(language: str, theme: str) -> Dict[str, Any]:
    default_context = {
        "logo": "ons-logo-pos-" + language,
        "logoAlt": lazy_gettext("Office for National Statistics logo"),
    }
    context = {
        "default": default_context,
        "social": default_context,
        "northernireland": default_context,
        "census": {
            **default_context,
            "titleLogo": f"census-logo-{language}",
            "titleLogoAlt": lazy_gettext("Census 2021"),
        },
        "census-nisra": {
            "logo": "nisra-logo-en",
            "mobileLogo": "nisra-logo-en-mobile",
            "logoAlt": lazy_gettext(
                "Northern Ireland Statistics and Research Agency logo"
            ),
            "titleLogo": "census-logo-en",
            "titleLogoAlt": lazy_gettext("Census 2021"),
            "customHeaderLogo": "nisra",
        },
    }
    return context.get(theme, {})


def get_footer_context(
    language_code: str, static_content_urls: Mapping, sign_out_url: str, theme: str
) -> Optional[Dict[str, Any]]:

    items_list = [
        {
            "text": lazy_gettext("Help"),
            "url": static_content_urls["help"],
            "target": "_blank",
        },
        {
            "text": lazy_gettext("Contact us"),
            "url": static_content_urls["contact_us"],
            "target": "_blank",
        },
    ]
    if theme != "census-nisra":
        items_list.extend(
            [
                {
                    "text": lazy_gettext("Languages"),
                    "url": static_content_urls["languages"],
                    "target": "_blank",
                },
                {
                    "text": lazy_gettext("BSL and audio videos"),
                    "url": static_content_urls["bsl_and_audio_videos"],
                    "target": "_blank",
                },
            ]
        )

    default_context = {
        "lang": language_code,
        "crest": True,
        "newTabWarning": lazy_gettext("The following links open in a new tab"),
        "copyrightDeclaration": {
            "copyright": lazy_gettext(
                "Crown copyright and database rights 2021 NIMA MOU577.501."
            )
            if theme == "census-nisra"
            else lazy_gettext("Crown copyright and database rights 2020 OS 100019153."),
            "text": lazy_gettext(
                "Use of address data is subject to the terms and conditions."
            ),
        },
        "rows": [
            {"itemsList": items_list},
        ],
        "legal": [
            {
                "itemsList": [
                    {
                        "text": lazy_gettext("Cookies"),
                        "url": static_content_urls["cookies"],
                        "target": "_blank",
                    },
                    {
                        "text": lazy_gettext("Accessibility statement"),
                        "url": static_content_urls["accessibility_statement"],
                        "target": "_blank",
                    },
                    {
                        "text": lazy_gettext("Privacy and data protection"),
                        "url": static_content_urls["privacy_and_data_protection"],
                        "target": "_blank",
                    },
                    {
                        "text": lazy_gettext("Terms and conditions"),
                        "url": static_content_urls["terms_and_conditions"],
                        "target": "_blank",
                    },
                ],
            },
        ],
    }

    if request.blueprint == "post_submission":
        default_context["footerWarning"] = lazy_gettext(
            "Make sure you <a href='{sign_out_url}'>leave this page</a> or close your browser if using a shared device"
        ).format(sign_out_url=sign_out_url)

    context = {
        "default": {
            **default_context,
        },
        "social": {
            **default_context,
        },
        "northernireland": {
            **default_context,
        },
        "census": {
            **default_context,
        },
        "census-nisra": {
            **default_context,
            "lang": "en",
            "poweredBy": {
                "logo": "nisra-logo-black-en",
                "alt": "NISRA - Northern Ireland Statistics and Research Agency",
            },
        },
    }
    return context.get(theme)


def _map_theme(theme: str) -> str:
    """Maps a survey schema theme to a design system theme

    :param theme: A schema defined theme
    :returns: A design system theme
    """
    if theme and theme not in ["census", "census-nisra"]:
        return "main"
    return "census"


def render_template(template: str, **kwargs: Union[Mapping, bool, str]) -> str:
    template = f"{template.lower()}.html"
    theme = cookie_session.get("theme", DEFAULT_THEME)
    survey_title = lazy_gettext("Census 2021")
    language_code = get_locale().language
    page_header_context = get_page_header_context(language_code, theme)
    page_header_context.update({"title": survey_title})
    google_tag_manager_context = get_google_tag_manager_context()
    cdn_url = f'{current_app.config["CDN_URL"]}{current_app.config["CDN_ASSETS_PATH"]}'
    base_url = get_census_base_url(theme, language_code)
    include_csrf_token = request.url_rule and "POST" in request.url_rule.methods
    account_service_url = cookie_session.get(
        "account_service_url", f"{CENSUS_EN_BASE_URL}en/start"
    )
    sign_out_url = url_for("session.get_sign_out")
    static_content_urls = get_static_content_urls(language_code, base_url, theme)
    footer_context = get_footer_context(
        language_code,
        static_content_urls,
        sign_out_url,
        theme,
    )

    return flask_render_template(
        template,
        account_service_url=account_service_url,
        account_service_log_out_url=cookie_session.get("account_service_log_out_url"),
        contact_us_url=static_content_urls["contact_us"],
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


def get_census_base_url(schema_theme: str, language_code: str) -> str:
    if language_code == "cy":
        return CENSUS_CY_BASE_URL

    if schema_theme == "census-nisra":
        return CENSUS_NIR_BASE_URL

    return CENSUS_EN_BASE_URL


@lru_cache(maxsize=None)
def get_static_content_urls(
    language_code: str, base_url: str, schema_theme: str
) -> Mapping:
    is_nisra_theme = schema_theme == "census-nisra"
    if language_code == "cy":
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
        help_path = (
            "help/help-with-the-questions/online-questions-help/"
            if is_nisra_theme
            else "help/how-to-answer-questions/online-questions-help/"
        )
        cookies_path = "cookies/"
        accessibility_statement_path = "accessibility-statement/"
        privacy_and_data_protection_path = "privacy-and-data-protection/"
        terms_and_conditions_path = "terms-and-conditions/"
        contact_us = "contact-us/"
        languages = "help/languages-and-accessibility/languages/"
        bsl_and_audio_videos = (
            "help/languages-and-accessibility/accessibility/accessible-videos-with-bsl/"
        )
    urls = {
        "help": f"{base_url}{help_path}",
        "cookies": f"{base_url}{cookies_path}",
        "accessibility_statement": f"{base_url}{accessibility_statement_path}",
        "privacy_and_data_protection": f"{base_url}{privacy_and_data_protection_path}",
        "terms_and_conditions": f"{base_url}{terms_and_conditions_path}",
        "contact_us": f"{base_url}{contact_us}",
    }
    if not is_nisra_theme:
        urls["languages"] = f"{base_url}{languages}"
        urls["bsl_and_audio_videos"] = f"{base_url}{bsl_and_audio_videos}"

    return urls


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


def get_data_layer(schema_theme: str) -> List:
    if schema_theme == "census-nisra":
        return [{"nisra": True}]

    if schema_theme == "census":
        return [{"nisra": False}]

    return []
