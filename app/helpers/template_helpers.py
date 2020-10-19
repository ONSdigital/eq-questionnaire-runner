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
    page_header_context = get_page_header_context(
        get_locale().language, theme or "census"
    )
    page_header_context.update({"title": survey_title})
    google_tag_manager_context = get_google_tag_manager_context()
    cdn_url = f'{current_app.config["CDN_URL"]}{current_app.config["CDN_ASSETS_PATH"]}'
    contact_us_url = get_contact_us_url(theme, get_locale().language)
    include_csrf_token = request.url_rule and "POST" in request.url_rule.methods
    account_service_url = cookie_session.get(
        "account_service_url", f"{CENSUS_BASE_URL}en/start"
    )

    return flask_render_template(
        template,
        account_service_url=account_service_url,
        account_service_log_out_url=cookie_session.get("account_service_log_out_url"),
        contact_us_url=contact_us_url,
        cookie_settings_url=current_app.config["COOKIE_SETTINGS_URL"],
        page_header=page_header_context,
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
        sign_out_url=url_for("session.get_sign_out"),
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


def get_contact_us_url(schema_theme: str, language_code: str):
    base_url = get_census_base_url(schema_theme, language_code)

    if language_code == "cy":
        return f"{base_url}cysylltu-a-ni/"

    return f"{base_url}contact-us/"


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
