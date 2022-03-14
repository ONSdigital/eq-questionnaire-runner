from typing import Type

import pytest
from flask import Flask, current_app

from app.helpers.template_helpers import ContextHelper, get_survey_config
from app.settings import ACCOUNT_SERVICE_BASE_URL
from app.survey_config import (
    BusinessSurveyConfig,
    CensusNISRASurveyConfig,
    CensusSurveyConfig,
    NorthernIrelandBusinessSurveyConfig,
    SurveyConfig,
    WelshCensusSurveyConfig,
)


def test_footer_context_census_theme(app: Flask, expected_footer_census_theme):
    with app.app_context():
        survey_config = CensusSurveyConfig()
        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["footer"]

    assert result == expected_footer_census_theme


def test_footer_context_business_theme(app: Flask, expected_footer_business_theme):
    with app.test_client():
        survey_config = BusinessSurveyConfig()

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["footer"]

    assert result == expected_footer_business_theme


def test_footer_warning_in_context_census_theme(app: Flask):
    with app.app_context():
        expected = "Make sure you <a href='/sign-out'>leave this page</a> or close your browser if using a shared device"

        survey_config = CensusSurveyConfig()

        result = ContextHelper(
            language="en",
            is_post_submission=True,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["footer"]["footerWarning"]

    assert result == expected


def test_footer_warning_not_in_context_census_theme(app: Flask):
    with app.app_context():
        with pytest.raises(KeyError):
            _ = ContextHelper(
                language="en",
                is_post_submission=False,
                include_csrf_token=True,
                survey_config=CensusSurveyConfig(),
            ).context["footer"]["footerWarning"]


def test_footer_context_census_nisra_theme(app: Flask, expected_footer_nisra_theme):
    with app.app_context():
        survey_config = CensusNISRASurveyConfig()

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["footer"]

    assert result == expected_footer_nisra_theme


def test_get_page_header_context_business(app: Flask):
    expected = {
        "logo": "ons-logo-en",
        "logoAlt": "Office for National Statistics logo",
    }

    with app.app_context():
        survey_config = SurveyConfig()

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["page_header"]

    assert result == expected


def test_get_page_header_context_census(app: Flask):
    expected = {
        "title": "Census 2021",
        "logo": "ons-logo-en",
        "logoAlt": "Office for National Statistics logo",
        "titleLogo": "census-logo-en",
        "titleLogoAlt": "Census 2021",
    }

    with app.app_context():
        survey_config = CensusSurveyConfig()

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["page_header"]

    assert result == expected


def test_get_page_header_context_census_nisra(app: Flask):
    expected = {
        "title": "Census 2021",
        "logo": "nisra-logo-en",
        "logoAlt": "Northern Ireland Statistics and Research Agency logo",
        "titleLogo": "census-logo-en",
        "titleLogoAlt": "Census 2021",
        "customHeaderLogo": True,
        "mobileLogo": "nisra-logo-en-mobile",
    }

    with app.app_context():
        survey_config = CensusNISRASurveyConfig()

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["page_header"]

    assert result == expected


@pytest.mark.parametrize(
    "survey_config, is_authenticated, expected",
    [
        (
            SurveyConfig(),
            True,
            None,
        ),
        (
            BusinessSurveyConfig(),
            True,
            {
                "itemsList": [
                    {
                        "title": "My account",
                        "url": "https://surveys.ons.gov.uk/my-account",
                        "id": "header-link-my-account",
                    },
                    {
                        "title": "Sign out",
                        "url": "/sign-out",
                        "id": "header-link-sign-out",
                    },
                ]
            },
        ),
    ],
)
def test_service_links_context(
    app: Flask, mocker, survey_config, is_authenticated, expected
):
    with app.app_context():
        current_user = mocker.patch(
            "flask_login.utils._get_user", return_value=mocker.MagicMock()
        )
        current_user.is_authenticated = is_authenticated

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["service_links"]

    assert result == expected


@pytest.mark.parametrize(
    "survey_config, expected",
    [
        (
            SurveyConfig(),
            "https://surveys.ons.gov.uk/contact-us/",
        ),
        (
            BusinessSurveyConfig(),
            "https://surveys.ons.gov.uk/contact-us/",
        ),
        (
            NorthernIrelandBusinessSurveyConfig(),
            "https://surveys.ons.gov.uk/contact-us/",
        ),
    ],
)
def test_contact_us_url_context(
    app: Flask, survey_config: SurveyConfig, expected: dict[str, str]
):
    with app.app_context():
        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["contact_us_url"]

    assert result == expected


@pytest.mark.parametrize(
    "survey_config, expected",
    [
        (SurveyConfig(), "Save and sign out"),
        (CensusSurveyConfig(), "Save and complete later"),
    ],
)
def test_sign_out_button_text_context(
    app: Flask, survey_config: SurveyConfig, expected: dict[str, str]
):
    with app.app_context():
        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["sign_out_button_text"]

    assert result == expected


@pytest.mark.parametrize(
    "survey_config, expected",
    [
        (SurveyConfig(), "https://surveys.ons.gov.uk/cookies/"),
        (
            BusinessSurveyConfig(),
            "https://surveys.ons.gov.uk/cookies/",
        ),
        (
            NorthernIrelandBusinessSurveyConfig(),
            "https://surveys.ons.gov.uk/cookies/",
        ),
    ],
)
def test_cookie_settings_url_context(
    app: Flask, survey_config: SurveyConfig, expected: str
):
    with app.app_context():
        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["cookie_settings_url"]

    assert result == expected


@pytest.mark.parametrize(
    "survey_config, expected",
    [
        (SurveyConfig(), None),
        (
            BusinessSurveyConfig(),
            "https://surveys.ons.gov.uk/my-account",
        ),
    ],
)
def test_account_service_my_account_url_context(
    app: Flask, survey_config: SurveyConfig, expected: str, get_context_helper
):
    result = get_context_helper(app, survey_config).context[
        "account_service_my_account_url"
    ]

    assert result == expected


@pytest.mark.parametrize(
    "survey_config, expected",
    [
        (SurveyConfig(), None),
        (
            BusinessSurveyConfig(),
            "https://surveys.ons.gov.uk/surveys/todo",
        ),
    ],
)
def test_account_service_my_todo_url_context(
    app: Flask, survey_config: SurveyConfig, expected: str, get_context_helper
):
    result = get_context_helper(app, survey_config).context["account_service_todo_url"]
    assert result == expected


@pytest.mark.parametrize(
    "survey_config, expected",
    [
        (SurveyConfig(), None),
        (
            BusinessSurveyConfig(),
            "https://surveys.ons.gov.uk/sign-in/logout",
        ),
        (CensusSurveyConfig(), "https://census.gov.uk/en/start"),
        (WelshCensusSurveyConfig(), "https://cyfrifiad.gov.uk/en/start"),
        (CensusNISRASurveyConfig(), "https://census.gov.uk/ni"),
        (
            NorthernIrelandBusinessSurveyConfig(),
            "https://surveys.ons.gov.uk/sign-in/logout",
        ),
    ],
)
def test_account_service_log_out_url_context(
    app: Flask, survey_config: SurveyConfig, expected: str, get_context_helper
):
    result = get_context_helper(app, survey_config).context[
        "account_service_log_out_url"
    ]
    assert result == expected


@pytest.mark.parametrize(
    "theme, language, expected",
    [
        ("default", "en", SurveyConfig),
        ("default", "cy", SurveyConfig),
        ("business", "en", BusinessSurveyConfig),
        ("business", "cy", BusinessSurveyConfig),
        ("health", "en", SurveyConfig),
        ("health", "cy", SurveyConfig),
        ("social", "en", SurveyConfig),
        ("social", "cy", SurveyConfig),
        ("northernireland", "en", NorthernIrelandBusinessSurveyConfig),
        ("northernireland", "cy", NorthernIrelandBusinessSurveyConfig),
        ("census", "en", CensusSurveyConfig),
        ("census", "cy", WelshCensusSurveyConfig),
        ("census-nisra", "en", CensusNISRASurveyConfig),
        ("census-nisra", "cy", CensusNISRASurveyConfig),
        (None, None, BusinessSurveyConfig),
    ],
)
def test_get_survey_config(
    app: Flask, theme: str, language: str, expected: SurveyConfig
):
    with app.app_context():
        result = get_survey_config(theme=theme, language=language)
    assert isinstance(result, expected)


@pytest.mark.parametrize(
    "survey_config_type",
    [SurveyConfig, BusinessSurveyConfig],
)
def test_survey_config_base_url_provided_used_in_links(
    app: Flask, survey_config_type: Type[SurveyConfig]
):
    base_url = "http://localhost"
    with app.app_context():
        result = survey_config_type(base_url=base_url)

    assert result.base_url == "http://localhost"

    urls_to_check = [
        result.account_service_my_account_url,
        result.account_service_log_out_url,
        result.account_service_todo_url,
        result.cookie_settings_url,
        result.contact_us_url,
        result.privacy_and_data_protection_url,
    ]

    for url in urls_to_check:
        if url:
            assert base_url in url


def test_survey_config_base_url_duplicate_todo(app: Flask):
    base_url = "http://localhost/surveys/todo"
    with app.app_context():
        result = BusinessSurveyConfig(base_url=base_url)

    assert result.base_url == "http://localhost"

    assert result.account_service_log_out_url == "http://localhost/sign-in/logout"
    assert result.account_service_my_account_url == "http://localhost/my-account"
    assert result.account_service_todo_url == "http://localhost/surveys/todo"
    assert result.contact_us_url == "http://localhost/contact-us/"
    assert result.cookie_settings_url == "http://localhost/cookies/"
    assert (
        result.privacy_and_data_protection_url
        == "http://localhost/privacy-and-data-protection/"
    )


def test_get_survey_config_base_url_not_provided(app: Flask):
    with app.app_context():
        result = get_survey_config()

    assert result.base_url == ACCOUNT_SERVICE_BASE_URL


def test_context_set_from_app_config(app):
    with app.app_context():
        current_app.config["CDN_URL"] = "test-cdn-url"
        current_app.config["CDN_ASSETS_PATH"] = "/test-assets-path"
        current_app.config["ADDRESS_LOOKUP_API_URL"] = "test-address-lookup-api-url"
        current_app.config["EQ_GOOGLE_TAG_MANAGER_ID"] = "test-google-tag-manager-id"
        current_app.config[
            "EQ_GOOGLE_TAG_MANAGER_AUTH"
        ] = "test-google-tag-manager-auth"
        survey_config = SurveyConfig()

        context = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context

    assert context["cdn_url"] == "test-cdn-url/test-assets-path"
    assert context["address_lookup_api_url"] == "test-address-lookup-api-url"
    assert context["google_tag_manager_id"] == "test-google-tag-manager-id"
    assert context["google_tag_manager_auth"] == "test-google-tag-manager-auth"


@pytest.mark.parametrize(
    "theme, language, expected",
    [
        ("default", "en", None),
        ("business", "en", None),
        ("health", "en", None),
        ("social", "en", None),
        ("northernireland", "en", None),
        ("census", "en", "census"),
        ("census", "cy", "census"),
        ("census-nisra", "en", "census"),
    ],
)
def test_correct_theme_in_context(app: Flask, theme: str, language: str, expected: str):
    with app.app_context():
        survey_config = get_survey_config(theme=theme, language=language)
        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["theme"]
    assert result == expected


@pytest.mark.parametrize(
    "theme, language, expected",
    [
        ("default", "en", "ONS Business Surveys"),
        ("business", "en", "ONS Business Surveys"),
        ("health", "en", None),
        ("social", "en", None),
        ("northernireland", "en", "ONS Business Surveys"),
        ("census", "en", "Census 2021"),
        ("census", "cy", "Census 2021"),
        ("census-nisra", "en", "Census 2021"),
    ],
)
def test_correct_survey_title_in_context(
    app: Flask, theme: str, language: str, expected: str
):
    with app.app_context():
        survey_config = get_survey_config(theme=theme, language=language)
        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["survey_title"]
    assert result == expected


@pytest.mark.parametrize(
    "theme, language, expected",
    [
        ("default", "en", []),
        ("business", "en", []),
        ("health", "en", []),
        ("social", "en", []),
        ("northernireland", "en", []),
        ("census", "en", [{"nisra": False}]),
        ("census", "cy", [{"nisra": False}]),
        ("census-nisra", "en", [{"nisra": True}]),
    ],
)
def test_correct_data_layer_in_context(
    app: Flask, theme: str, language: str, expected: str
):
    with app.app_context():
        survey_config = get_survey_config(theme=theme, language=language)

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["data_layer"]
    assert result == expected


@pytest.mark.parametrize(
    "include_csrf_token",
    [
        (False),
        (True),
    ],
)
def test_include_csrf_token(app: Flask, include_csrf_token: bool):
    with app.app_context():
        survey_config = SurveyConfig()

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=include_csrf_token,
            survey_config=survey_config,
        ).context["include_csrf_token"]

    assert result == include_csrf_token
