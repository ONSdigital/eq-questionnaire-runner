import pytest
from flask import Flask, current_app

from app.helpers.template_helpers import ContextHelper, get_survey_config
from app.survey_config import (
    BusinessSurveyConfig,
    CensusNISRASurveyConfig,
    CensusSurveyConfig,
    SurveyConfig,
    WelshCensusSurveyConfig,
)


def test_footer_context_census_theme(app: Flask):
    with app.app_context():
        expected = {
            "lang": "en",
            "crest": True,
            "newTabWarning": "The following links open in a new tab",
            "copyrightDeclaration": {
                "copyright": "Crown copyright and database rights 2020 OS 100019153.",
                "text": "Use of address data is subject to the terms and conditions.",
            },
            "rows": [
                {
                    "itemsList": [
                        {
                            "text": "Help",
                            "url": "https://census.gov.uk/help/how-to-answer-questions/online-questions-help/",
                            "target": "_blank",
                        },
                        {
                            "text": "Contact us",
                            "url": "https://census.gov.uk/contact-us/",
                            "target": "_blank",
                        },
                        {
                            "text": "Languages",
                            "url": "https://census.gov.uk/help/languages-and-accessibility/languages/",
                            "target": "_blank",
                        },
                        {
                            "text": "BSL and audio videos",
                            "url": "https://census.gov.uk/help/languages-and-accessibility/accessibility/accessible-videos-with-bsl/",
                            "target": "_blank",
                        },
                    ]
                }
            ],
            "legal": [
                {
                    "itemsList": [
                        {
                            "text": "Cookies",
                            "url": "https://census.gov.uk/cookies/",
                            "target": "_blank",
                        },
                        {
                            "text": "Accessibility statement",
                            "url": "https://census.gov.uk/accessibility-statement/",
                            "target": "_blank",
                        },
                        {
                            "text": "Privacy and data protection",
                            "url": "https://census.gov.uk/privacy-and-data-protection/",
                            "target": "_blank",
                        },
                        {
                            "text": "Terms and conditions",
                            "url": "https://census.gov.uk/terms-and-conditions/",
                            "target": "_blank",
                        },
                    ]
                }
            ],
        }

        survey_config = CensusSurveyConfig()

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["footer"]

    assert result == expected


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


def test_footer_context_census_nisra_theme(app: Flask):
    with app.app_context():
        expected = {
            "lang": "en",
            "crest": True,
            "newTabWarning": "The following links open in a new tab",
            "copyrightDeclaration": {
                "copyright": "Crown copyright and database rights 2021 NIMA MOU577.501.",
                "text": "Use of address data is subject to the terms and conditions.",
            },
            "rows": [
                {
                    "itemsList": [
                        {
                            "text": "Help",
                            "url": "https://census.gov.uk/ni/help/help-with-the-questions/online-questions-help/",
                            "target": "_blank",
                        },
                        {
                            "text": "Contact us",
                            "url": "https://census.gov.uk/ni/contact-us/",
                            "target": "_blank",
                        },
                    ]
                }
            ],
            "legal": [
                {
                    "itemsList": [
                        {
                            "text": "Cookies",
                            "url": "https://census.gov.uk/ni/cookies/",
                            "target": "_blank",
                        },
                        {
                            "text": "Accessibility statement",
                            "url": "https://census.gov.uk/ni/accessibility-statement/",
                            "target": "_blank",
                        },
                        {
                            "text": "Privacy and data protection",
                            "url": "https://census.gov.uk/ni/privacy-and-data-protection/",
                            "target": "_blank",
                        },
                        {
                            "text": "Terms and conditions",
                            "url": "https://census.gov.uk/ni/terms-and-conditions/",
                            "target": "_blank",
                        },
                    ]
                }
            ],
            "poweredBy": {
                "logo": "nisra-logo-black-en",
                "alt": "NISRA - Northern Ireland Statistics and Research Agency",
            },
        }

        survey_config = CensusNISRASurveyConfig()

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["footer"]

    assert result == expected


def test_get_page_header_context_business(app: Flask):
    expected = {
        "logo": "ons-logo-pos-en",
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
        "logo": "ons-logo-pos-en",
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
        "customHeaderLogo": "nisra",
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
    "survey_config,expected",
    [
        (
            SurveyConfig(),
            {
                "url": "https://ons.gov.uk/contact-us/",
                "text": "Contact us",
                "target": "_blank",
            },
        ),
        (
            BusinessSurveyConfig(),
            {
                "url": "https://surveys.ons.gov.uk/contact-us/",
                "text": "Contact us",
                "target": "_blank",
            },
        ),
        (
            CensusSurveyConfig(),
            {
                "url": "https://census.gov.uk/contact-us/",
                "text": "Contact us",
                "target": "_blank",
            },
        ),
        (
            WelshCensusSurveyConfig(),
            {
                "url": "https://cyfrifiad.gov.uk/contact-us/",
                "text": "Contact us",
                "target": "_blank",
            },
        ),
        (
            CensusNISRASurveyConfig(),
            {
                "url": "https://census.gov.uk/ni/contact-us/",
                "text": "Contact us",
                "target": "_blank",
            },
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
    "survey_config,expected",
    [
        (SurveyConfig(), None),
        (BusinessSurveyConfig(), "https://surveys.ons.gov.uk/surveys/todo"),
        (CensusSurveyConfig(), "https://census.gov.uk/en/start"),
        (WelshCensusSurveyConfig(), "https://cyfrifiad.gov.uk/en/start"),
        (CensusNISRASurveyConfig(), "https://census.gov.uk/ni"),
    ],
)
def test_account_service_url_context(
    app: Flask, survey_config: SurveyConfig, expected: str
):
    with app.app_context():
        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["account_service_url"]

    assert result == expected


@pytest.mark.parametrize(
    "theme,language,expected",
    [
        ("default", "en", SurveyConfig),
        ("default", "cy", SurveyConfig),
        ("business", "en", BusinessSurveyConfig),
        ("business", "cy", BusinessSurveyConfig),
        ("health", "en", SurveyConfig),
        ("health", "cy", SurveyConfig),
        ("social", "en", SurveyConfig),
        ("social", "cy", SurveyConfig),
        ("northernireland", "en", SurveyConfig),
        ("northernireland", "cy", SurveyConfig),
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


def test_context_set_from_app_config(app):
    with app.app_context():
        current_app.config["COOKIE_SETTINGS_URL"] = "test-cookie-settings-url"
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

    assert context["cookie_settings_url"] == "test-cookie-settings-url"
    assert context["cdn_url"] == "test-cdn-url/test-assets-path"
    assert context["address_lookup_api_url"] == "test-address-lookup-api-url"
    assert context["google_tag_manager_id"] == "test-google-tag-manager-id"
    assert context["google_tag_manager_auth"] == "test-google-tag-manager-auth"


@pytest.mark.parametrize(
    "theme,language,expected",
    [
        ("default", "en", "main"),
        ("business", "en", "main"),
        ("health", "en", "main"),
        ("social", "en", "main"),
        ("northernireland", "en", "main"),
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
    "theme,language,expected",
    [
        ("default", "en", None),
        ("business", "en", None),
        ("health", "en", None),
        ("social", "en", None),
        ("northernireland", "en", None),
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
    "theme,language,expected",
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
