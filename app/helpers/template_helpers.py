import re
from functools import lru_cache

from flask import current_app
from flask import render_template as flask_render_template
from flask import request
from flask import session as cookie_session
from flask import url_for
from flask_babel import get_locale, lazy_gettext

from app.helpers.language_helper import get_languages_context

CENSUS_BASE_URL = "https://census.gov.uk/"


@lru_cache(maxsize=None)
def get_page_header_context(language, theme):
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
            "mobileLogo": "nisra-logo-en",
            "logoAlt": lazy_gettext(
                "Northern Ireland Statistics and Research Agency logo"
            ),
            "titleLogo": "census-logo-en",
            "titleLogoAlt": lazy_gettext("Census 2021"),
            "customHeaderLogo": "nisra",
        },
    }
    return context.get(theme)


def get_footer_context(language_code, theme, base_url, contact_us_url, sign_out_url):
    footer_urls = get_footer_urls(language_code, theme)

    footer_warning = (
        lazy_gettext(
            f"Make sure you <a href='{sign_out_url}'>leave this page</a> or close your browser if using a shared device"
        )
        if request.blueprint == "post_submission"
        else None
    )

    default_context = {
        "crest": True,
        "newTabWarning": lazy_gettext("The following links open in a new tab"),
        "copyrightDeclaration": {
            "copyright": lazy_gettext(
                "Crown copyright and database rights 2020 OS 100019153."
            ),
            "text": lazy_gettext("Use of address data is subject to the"),
            "link": lazy_gettext("terms and conditions"),
            "url": f"{base_url}/{footer_urls['terms_and_conditions_path']}",
            "target": "_blank",
        },
        "footerWarning": footer_warning,
        "rows": [
            {
                "itemsList": [
                    {
                        "text": lazy_gettext("Help"),
                        "url": f"{base_url}/{footer_urls['help_path']}",
                        "target": "_blank",
                    },
                    {
                        "text": lazy_gettext("Contact us"),
                        "url": contact_us_url,
                        "target": "_blank",
                    },
                ]
            },
            {
                "itemsList": [
                    {
                        "text": lazy_gettext("Cookies"),
                        "url": f"{base_url}/{footer_urls['cookies_path']}",
                        "target": "_blank",
                    },
                    {
                        "text": lazy_gettext("Accessibility statement"),
                        "url": f"{base_url}/{footer_urls['accessibility_statement_path']}",
                        "target": "_blank",
                    },
                    {
                        "text": lazy_gettext("Privacy and data protection"),
                        "url": f"{base_url}/{footer_urls['privacy_and_data_protection_path']}",
                        "target": "_blank",
                    },
                    {
                        "text": lazy_gettext("Terms and conditions"),
                        "url": f"{base_url}/{footer_urls['terms_and_conditions_path']}",
                        "target": "_blank",
                    },
                ]
            },
        ],
    }
    context = {
        "census": {
            **default_context,
            "schema_theme": theme,
            "lang": language_code,
        },
        "census-nisra": {
            **default_context,
            "schema_theme": theme,
            "lang": "en",
            "poweredBy": {
                "logo": "nisra-logo-black-en",
                "alt": "NISRA - Northern Ireland Statistics and Research Agency",
            },
        },
    }
    return context.get(theme)


def _map_theme(theme):
    """Maps a survey schema theme to a design system theme

    :param theme: A schema defined theme
    :returns: A design system theme
    """
    if theme and theme not in ["census", "census-nisra"]:
        return "main"
    return "census"


def render_template(template, **kwargs):
    template = f"{template.lower()}.html"
    theme = cookie_session.get("theme")
    survey_title = lazy_gettext("Census 2021")
    language_code = get_locale().language
    page_header_context = get_page_header_context(language_code, theme or "census")
    page_header_context.update({"title": survey_title})
    google_tag_manager_context = get_google_tag_manager_context()
    cdn_url = f'{current_app.config["CDN_URL"]}{current_app.config["CDN_ASSETS_PATH"]}'
    base_url = get_census_base_url(theme, language_code)
    contact_us_url = get_contact_us_url(language_code, base_url)
    include_csrf_token = request.url_rule and "POST" in request.url_rule.methods
    account_service_url = cookie_session.get(
        "account_service_url", f"{CENSUS_BASE_URL}en/start"
    )
    sign_out_url = url_for("session.get_sign_out")
    footer_context = get_footer_context(
        language_code, theme, base_url, contact_us_url, sign_out_url
    )

    return flask_render_template(
        template,
        account_service_url=account_service_url,
        account_service_log_out_url=cookie_session.get("account_service_log_out_url"),
        contact_us_url=contact_us_url,
        cookie_settings_url=current_app.config["COOKIE_SETTINGS_URL"],
        page_header=page_header_context,
        footer=footer_context,
        theme=_map_theme(theme),
        languages=get_languages_context(),
        schema_theme=theme,
        language_code=get_locale().language,
        survey_title=survey_title,
        cdn_url=cdn_url,
        csp_nonce=request.csp_nonce,
        address_lookup_api_url=current_app.config["ADDRESS_LOOKUP_API_URL"],
        data_layer=get_data_layer(theme),
        include_csrf_token=include_csrf_token,
        sign_out_url=sign_out_url,
        **google_tag_manager_context,
        **kwargs,
    )


def get_google_tag_manager_context():
    cookie = request.cookies.get("ons_cookie_policy")
    if cookie and "'usage':true" in cookie:
        return {
            "google_tag_manager_id": current_app.config["EQ_GOOGLE_TAG_MANAGER_ID"],
            "google_tag_manager_auth": current_app.config["EQ_GOOGLE_TAG_MANAGER_AUTH"],
            "google_tag_manager_preview": current_app.config[
                "EQ_GOOGLE_TAG_MANAGER_PREVIEW"
            ],
        }
    return {}


def get_census_base_url(schema_theme: str, language_code: str) -> str:
    if language_code == "cy":
        return "https://cyfrifiad.gov.uk/"

    if schema_theme == "census-nisra":
        return f"{CENSUS_BASE_URL}ni/"

    return CENSUS_BASE_URL


def get_contact_us_url(language_code: str, base_url: str):
    if language_code == "cy":
        return f"{base_url}cysylltu-a-ni/"

    return f"{base_url}contact-us/"


def get_footer_urls(language_code: str, schema_theme: str):
    if language_code == "cy":
        return {
            "help_path": "help/sut-i-ateb-y-cwestiynau/help-y-cwestiynau-ar-lein/",
            "cookies_path": "cwcis/",
            "accessibility_statement_path": "hygyrchedd/",
            "privacy_and_data_protection_path": "preifatrwydd-a-diogelu-data/",
            "terms_and_conditions_path": "telerau-ac-amodau/",
        }
    else:
        help_path = (
            "help/help-with-the-questions/online-questions-help/"
            if schema_theme == "census-nisra"
            else "help/how-to-answer-questions/online-questions-help/"
        )

        return {
            "help_path": help_path,
            "cookies_path": "cookies/",
            "accessibility_statement_path": "accessibility/",
            "privacy_and_data_protection_path": "privacy-and-data-protection/",
            "terms_and_conditions_path": "terms-and-conditions/",
        }


def safe_content(content):
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


def get_data_layer(schema_theme):
    if schema_theme == "census-nisra":
        return [{"nisra": True}]

    if schema_theme == "census":
        return [{"nisra": False}]

    return []
