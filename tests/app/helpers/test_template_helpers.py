import pytest
from flask import Flask, current_app

from app.helpers.template_helpers import (
    CensusNISRASurveyConfig,
    CensusSurveyConfig,
    ContextHelper,
    SurveyConfig,
    WelshCensusSurveyConfig,
    get_survey_config,
)
from app.setup import create_app


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
        ("business", "en", SurveyConfig),
        ("business", "cy", SurveyConfig),
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
