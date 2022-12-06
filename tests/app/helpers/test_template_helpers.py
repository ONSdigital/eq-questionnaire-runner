from typing import Type

import pytest
from flask import Flask, current_app
from flask import session as cookie_session

from app.helpers.template_helpers import ContextHelper, get_survey_config
from app.questionnaire import QuestionnaireSchema
from app.settings import (
    ACCOUNT_SERVICE_BASE_URL,
    ACCOUNT_SERVICE_BASE_URL_SOCIAL,
    ONS_URL,
    ONS_URL_CY,
    read_file,
)
from app.survey_config import (
    BusinessSurveyConfig,
    CensusNISRASurveyConfig,
    CensusSurveyConfig,
    NorthernIrelandBusinessSurveyConfig,
    SocialSurveyConfig,
    SurveyConfig,
    WelshCensusSurveyConfig,
)
from app.survey_config.survey_type import SurveyType
from tests.app.helpers.conftest import (
    expected_footer_business_theme,
    expected_footer_business_theme_no_cookie,
    expected_footer_census_theme,
    expected_footer_census_theme_no_cookie,
    expected_footer_census_welsh_theme,
    expected_footer_nisra_theme,
    expected_footer_social_theme,
    expected_footer_social_theme_no_cookie,
)
from tests.app.questionnaire.conftest import get_metadata

DEFAULT_URL = "http://localhost"


@pytest.mark.parametrize(
    "theme, survey_config, language, expected_footer",
    [
        (SurveyType.CENSUS, CensusSurveyConfig(), "en", expected_footer_census_theme()),
        (None, CensusSurveyConfig(), "en", expected_footer_census_theme_no_cookie()),
        (
            SurveyType.BUSINESS,
            BusinessSurveyConfig(),
            "en",
            expected_footer_business_theme(),
        ),
        (
            None,
            BusinessSurveyConfig(),
            "en",
            expected_footer_business_theme_no_cookie(),
        ),
        (
            SurveyType.SOCIAL,
            SocialSurveyConfig(),
            "en",
            expected_footer_social_theme("en"),
        ),
        (None, SocialSurveyConfig(), "en", expected_footer_social_theme_no_cookie()),
        (
            SurveyType.SOCIAL,
            SocialSurveyConfig(language_code="cy"),
            "cy",
            expected_footer_social_theme("cy"),
        ),
        (
            SurveyType.CENSUS_NISRA,
            CensusNISRASurveyConfig(),
            "en",
            expected_footer_nisra_theme(),
        ),
        (
            SurveyType.CENSUS,
            WelshCensusSurveyConfig(),
            "en",
            expected_footer_census_welsh_theme(),
        ),
    ],
)
def test_footer_context(app: Flask, theme, survey_config, language, expected_footer):
    with app.app_context():
        if theme:
            cookie_session["theme"] = theme
        config = survey_config

        result = ContextHelper(
            language=language,
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=config,
        ).context["footer"]

    assert result == expected_footer


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


@pytest.mark.parametrize(
    "theme, survey_title, survey_config, expected",
    (
        (
            SurveyType.BUSINESS,
            None,
            BusinessSurveyConfig(),
            ["ONS Business Surveys", None, None],
        ),
        (
            SurveyType.BUSINESS,
            "Test",
            BusinessSurveyConfig(),
            ["Test", None, None],
        ),
        (
            None,
            None,
            BusinessSurveyConfig(),
            ["ONS Business Surveys", None, None],
        ),
        (
            SurveyType.SOCIAL,
            None,
            SocialSurveyConfig(),
            ["ONS Social Surveys", None, None],
        ),
        (
            SurveyType.SOCIAL,
            "Test",
            SocialSurveyConfig(),
            ["Test", None, None],
        ),
        (
            SurveyType.SOCIAL,
            "Test",
            SocialSurveyConfig(language_code="cy"),
            ["Test", None, None],
        ),
        (
            None,
            None,
            SocialSurveyConfig(),
            ["ONS Social Surveys", None, None],
        ),
        (
            None,
            None,
            SurveyConfig(),
            [None, None, None],
        ),
        (
            SurveyType.CENSUS,
            None,
            CensusSurveyConfig(),
            ["Census 2021", None, None],
        ),
        (
            SurveyType.CENSUS,
            "Test",
            CensusSurveyConfig(),
            ["Test", None, None],
        ),
        (
            None,
            None,
            CensusSurveyConfig(),
            ["Census 2021", None, None],
        ),
        (
            SurveyType.CENSUS_NISRA,
            None,
            CensusNISRASurveyConfig(),
            ["Census 2021", None, None],
        ),
        (
            None,
            None,
            CensusNISRASurveyConfig(),
            ["Census 2021", None, None],
        ),
        (
            None,
            None,
            NorthernIrelandBusinessSurveyConfig(),
            [
                "ONS Business Surveys",
                read_file("./templates/assets/images/ni-finance-logo.svg"),
                read_file("./templates/assets/images/ni-finance-mobile-logo.svg"),
            ],
        ),
    ),
)
def test_header_context(app: Flask, theme, survey_title, survey_config, expected):
    with app.app_context():
        for cookie_name, cookie_value in {
            "theme": theme,
            "survey_title": survey_title,
        }.items():
            if cookie_value:
                cookie_session[cookie_name] = cookie_value

        context_helper = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        )

        result = [
            context_helper.context["survey_title"],
            context_helper.context["mastheadLogo"],
            context_helper.context["mastheadLogoMobile"],
        ]

    assert result == expected


@pytest.mark.parametrize(
    "survey_config, is_authenticated, theme, expected",
    [
        (
            SurveyConfig(),
            True,
            None,
            None,
        ),
        (
            BusinessSurveyConfig(),
            False,
            "business",
            {
                "toggleServicesButton": {
                    "text": "Menu",
                    "ariaLabel": "Toggle services menu",
                },
                "itemsList": [
                    {
                        "title": "Help",
                        "url": f"{ACCOUNT_SERVICE_BASE_URL}/help",
                        "id": "header-link-help",
                    }
                ],
            },
        ),
        (
            BusinessSurveyConfig(schema=QuestionnaireSchema({"survey_id": "001"})),
            True,
            "business",
            {
                "toggleServicesButton": {
                    "text": "Menu",
                    "ariaLabel": "Toggle services menu",
                },
                "itemsList": [
                    {
                        "title": "Help",
                        "url": f"{ACCOUNT_SERVICE_BASE_URL}/surveys/surveys-help?survey_ref=001&ru_ref=63782964754",
                        "id": "header-link-help",
                    },
                    {
                        "title": "My account",
                        "url": f"{ACCOUNT_SERVICE_BASE_URL}/my-account",
                        "id": "header-link-my-account",
                    },
                    {
                        "title": "Sign out",
                        "url": "/sign-out",
                        "id": "header-link-sign-out",
                    },
                ],
            },
        ),
        (SocialSurveyConfig(), False, None, None),
        (
            SocialSurveyConfig(schema=QuestionnaireSchema({"survey_id": "001"})),
            True,
            "social",
            None,
        ),
    ],
)
def test_service_links_context(
    app: Flask, mocker, survey_config, is_authenticated, theme, expected
):
    with app.app_context():
        mocked_current_user = mocker.Mock()
        mocked_current_user.is_authenticated = is_authenticated
        mocker.patch("flask_login.utils._get_user", return_value=mocked_current_user)
        cookie_session["theme"] = theme

        if is_authenticated:
            mocker.patch(
                "app.helpers.template_helpers.get_metadata",
                return_value=get_metadata({"ru_ref": "63782964754U", "tx_id": "tx_id"}),
            )

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["service_links"]

    assert result == expected


@pytest.mark.parametrize(
    "survey_config, language, expected",
    [
        (
            SurveyConfig(),
            "en",
            f"{ACCOUNT_SERVICE_BASE_URL}/contact-us/",
        ),
        (
            BusinessSurveyConfig(),
            "en",
            f"{ACCOUNT_SERVICE_BASE_URL}/contact-us/",
        ),
        (
            NorthernIrelandBusinessSurveyConfig(),
            "en",
            f"{ACCOUNT_SERVICE_BASE_URL}/contact-us/",
        ),
        (
            SocialSurveyConfig(),
            "en",
            f"{ONS_URL}/aboutus/contactus/surveyenquiries/",
        ),
        (
            SocialSurveyConfig(language_code="cy"),
            "cy",
            f"{ONS_URL_CY}/aboutus/contactus/surveyenquiries/",
        ),
    ],
)
def test_contact_us_url_context(
    app: Flask,
    survey_config: SurveyConfig,
    language: str,
    expected: dict[str, str],
):
    with app.app_context():
        result = ContextHelper(
            language=language,
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["contact_us_url"]

    assert result == expected


@pytest.mark.parametrize(
    "survey_config, expected",
    [
        (SurveyConfig(), "Save and exit survey"),
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
    "survey_config, cookie_present, expected",
    [
        (SurveyConfig(), True, f"{ACCOUNT_SERVICE_BASE_URL}/cookies/"),
        (
            BusinessSurveyConfig(),
            True,
            f"{ACCOUNT_SERVICE_BASE_URL}/cookies/",
        ),
        (
            NorthernIrelandBusinessSurveyConfig(),
            True,
            f"{ACCOUNT_SERVICE_BASE_URL}/cookies/",
        ),
        (
            SocialSurveyConfig(),
            True,
            f"{ACCOUNT_SERVICE_BASE_URL_SOCIAL}/en/cookies/",
        ),
        (
            SocialSurveyConfig(language_code="cy"),
            True,
            f"{ACCOUNT_SERVICE_BASE_URL_SOCIAL}/cy/cookies/",
        ),
        (SurveyConfig(), False, None),
    ],
)
def test_cookie_settings_url_context(
    app: Flask, survey_config: SurveyConfig, cookie_present: bool, expected: str
):
    with app.app_context():
        if cookie_present:
            cookie_session["theme"] = "dummy_value"
        context_helper = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        )
        result = context_helper.context.get("cookie_settings_url")

    assert result == expected


@pytest.mark.parametrize(
    "survey_config, language, address",
    [
        (SurveyConfig(), "en", ACCOUNT_SERVICE_BASE_URL),
        (
            BusinessSurveyConfig(),
            "en",
            ACCOUNT_SERVICE_BASE_URL,
        ),
        (
            NorthernIrelandBusinessSurveyConfig(),
            "en",
            ACCOUNT_SERVICE_BASE_URL,
        ),
        (
            SocialSurveyConfig(),
            "en",
            ACCOUNT_SERVICE_BASE_URL_SOCIAL,
        ),
        (
            SocialSurveyConfig(),
            "cy",
            ACCOUNT_SERVICE_BASE_URL_SOCIAL,
        ),
    ],
)
def test_cookie_domain_context(
    app: Flask, survey_config: SurveyConfig, language: str, address: str
):
    with app.app_context():
        cookie_session["theme"] = "dummy_value"
        context_helper = ContextHelper(
            language=language,
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        )

        expected = address.replace("https://", "")
        result = context_helper.context.get("cookie_domain")

    assert result == expected


@pytest.mark.parametrize(
    "survey_config",
    [
        SurveyConfig(),
        BusinessSurveyConfig(),
        NorthernIrelandBusinessSurveyConfig(),
        SocialSurveyConfig(),
    ],
)
def test_cookie_domain_context_cookie_not_provided(
    app: Flask, survey_config: SurveyConfig
):
    with app.app_context():
        context_helper = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        )

    assert "cookie_domain" not in context_helper.context


@pytest.mark.parametrize(
    "survey_config, expected",
    [
        (SurveyConfig(), None),
        (
            BusinessSurveyConfig(),
            f"{ACCOUNT_SERVICE_BASE_URL}/my-account",
        ),
        (SocialSurveyConfig(), None),
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
            f"{ACCOUNT_SERVICE_BASE_URL}/surveys/todo",
        ),
        (
            SocialSurveyConfig(),
            None,
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
            f"{ACCOUNT_SERVICE_BASE_URL}/sign-in/logout",
        ),
        (CensusSurveyConfig(), "https://census.gov.uk/en/start"),
        (WelshCensusSurveyConfig(), "https://cyfrifiad.gov.uk/en/start"),
        (CensusNISRASurveyConfig(), "https://census.gov.uk/ni"),
        (
            NorthernIrelandBusinessSurveyConfig(),
            f"{ACCOUNT_SERVICE_BASE_URL}/sign-in/logout",
        ),
        (
            SocialSurveyConfig(),
            f"{ACCOUNT_SERVICE_BASE_URL_SOCIAL}/en/start/",
        ),
        (
            SocialSurveyConfig(language_code="cy"),
            f"{ACCOUNT_SERVICE_BASE_URL_SOCIAL}/cy/start/",
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
        (SurveyType.DEFAULT, "en", SurveyConfig),
        (SurveyType.DEFAULT, "cy", SurveyConfig),
        (SurveyType.BUSINESS, "en", BusinessSurveyConfig),
        (SurveyType.BUSINESS, "cy", BusinessSurveyConfig),
        (SurveyType.HEALTH, "en", SocialSurveyConfig),
        (SurveyType.SOCIAL, "en", SocialSurveyConfig),
        (SurveyType.NORTHERN_IRELAND, "en", NorthernIrelandBusinessSurveyConfig),
        (SurveyType.NORTHERN_IRELAND, "cy", NorthernIrelandBusinessSurveyConfig),
        (SurveyType.CENSUS, "en", CensusSurveyConfig),
        (SurveyType.CENSUS, "cy", WelshCensusSurveyConfig),
        (SurveyType.CENSUS_NISRA, "en", CensusNISRASurveyConfig),
        (SurveyType.CENSUS_NISRA, "cy", CensusNISRASurveyConfig),
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
    "survey_config_type, base_url",
    [
        (SocialSurveyConfig, ACCOUNT_SERVICE_BASE_URL_SOCIAL),
        (SurveyConfig, DEFAULT_URL),
        (BusinessSurveyConfig, DEFAULT_URL),
    ],
)
def test_survey_config_base_url_provided_used_in_links(
    app: Flask, survey_config_type: Type[SurveyConfig], base_url: str
):
    with app.app_context():
        result = survey_config_type(base_url=base_url)

    assert result.base_url == base_url

    urls_to_check = [
        result.account_service_my_account_url,
        result.account_service_log_out_url,
        result.account_service_todo_url,
        result.cookie_settings_url,
        result.contact_us_url,
        result.privacy_and_data_protection_url,
    ]

    if survey_config_type == SocialSurveyConfig:

        urls_to_check.remove(result.contact_us_url)

    for url in urls_to_check:
        if url:
            assert base_url in url


def test_survey_config_base_url_duplicate_todo(app: Flask):
    base_url = f"{DEFAULT_URL}/surveys/todo"
    with app.app_context():
        result = BusinessSurveyConfig(base_url=base_url)

    assert result.base_url == DEFAULT_URL

    assert result.account_service_log_out_url == f"{DEFAULT_URL}/sign-in/logout"
    assert result.account_service_my_account_url == f"{DEFAULT_URL}/my-account"
    assert result.account_service_todo_url == f"{DEFAULT_URL}/surveys/todo"
    assert result.contact_us_url == f"{DEFAULT_URL}/contact-us/"
    assert result.cookie_settings_url == f"{DEFAULT_URL}/cookies/"
    assert (
        result.privacy_and_data_protection_url
        == f"{DEFAULT_URL}/privacy-and-data-protection/"
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
        (SurveyType.DEFAULT, "en", None),
        (SurveyType.BUSINESS, "en", None),
        (SurveyType.HEALTH, "en", None),
        (SurveyType.SOCIAL, "en", None),
        (SurveyType.SOCIAL, "cy", None),
        (SurveyType.NORTHERN_IRELAND, "en", None),
        (SurveyType.CENSUS, "en", "census"),
        (SurveyType.CENSUS, "cy", "census"),
        (SurveyType.CENSUS_NISRA, "en", "census"),
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
        (SurveyType.DEFAULT, "en", "ONS Business Surveys"),
        (SurveyType.BUSINESS, "en", "ONS Business Surveys"),
        (SurveyType.HEALTH, "en", "ONS Social Surveys"),
        (SurveyType.SOCIAL, "en", "ONS Social Surveys"),
        (SurveyType.SOCIAL, "cy", "ONS Social Surveys"),
        (SurveyType.NORTHERN_IRELAND, "en", "ONS Business Surveys"),
        (SurveyType.CENSUS, "en", "Census 2021"),
        (SurveyType.CENSUS, "cy", "Census 2021"),
        (SurveyType.CENSUS_NISRA, "en", "Census 2021"),
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
    "theme, language, schema, expected",
    [
        (
            SurveyType.DEFAULT,
            "en",
            QuestionnaireSchema({"survey_id": "001"}),
            [{"survey_id": "001"}],
        ),
        (
            SurveyType.DEFAULT,
            "en",
            QuestionnaireSchema({"survey_id": "001", "form_type": "test"}),
            [{"form_type": "test", "survey_id": "001"}],
        ),
        (
            SurveyType.BUSINESS,
            "en",
            QuestionnaireSchema(
                {"survey_id": "001", "form_type": "test", "title": "test_title"}
            ),
            [{"form_type": "test", "survey_id": "001", "title": "test_title"}],
        ),
        (
            SurveyType.HEALTH,
            "en",
            QuestionnaireSchema({"survey_id": "001"}),
            [{"survey_id": "001"}],
        ),
        (
            SurveyType.SOCIAL,
            "en",
            QuestionnaireSchema({"survey_id": "001"}),
            [{"survey_id": "001"}],
        ),
        (
            SurveyType.NORTHERN_IRELAND,
            "en",
            QuestionnaireSchema({"survey_id": "001"}),
            [{"survey_id": "001"}],
        ),
        (
            SurveyType.CENSUS,
            "en",
            QuestionnaireSchema({"survey_id": "001"}),
            [{"nisra": False}],
        ),
        (
            SurveyType.CENSUS,
            "cy",
            QuestionnaireSchema({"survey_id": "001"}),
            [{"nisra": False}],
        ),
        (
            SurveyType.CENSUS_NISRA,
            QuestionnaireSchema({"survey_id": "001"}),
            "en",
            [{"nisra": True}],
        ),
    ],
)
def test_correct_data_layer_in_context(
    app: Flask, theme: str, language: str, schema: QuestionnaireSchema, expected: str
):
    with app.app_context():
        survey_config = get_survey_config(theme=theme, language=language, schema=schema)

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
