from datetime import datetime, timezone

import pytest
from pytest import fixture

from app.data_models import SessionData, SessionStore
from app.helpers.template_helpers import ContextHelper


@fixture
def get_context_helper():
    def _context_helper(
        app, survey_config, is_post_submission=False, include_csrf_token=True
    ):
        with app.test_client():
            return ContextHelper(
                language="en",
                is_post_submission=is_post_submission,
                include_csrf_token=include_csrf_token,
                survey_config=survey_config,
            )

    return _context_helper


@fixture(name="footer_context")
def footer():
    return {
        "lang": "en",
        "crest": True,
        "newTabWarning": "The following links open in a new tab",
        "copyrightDeclaration": {
            "copyright": "Crown copyright and database rights 2020 OS 100019153.",
            "text": "Use of address data is subject to the terms and conditions.",
        },
    }


@fixture
def expected_footer_census_theme(footer_context):
    census = {
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
    return {**footer_context, **census}


@fixture
def expected_footer_business_theme(footer_context):
    business = {
        "rows": [
            {
                "itemsList": [
                    {
                        "text": "What we do",
                        "url": "https://www.ons.gov.uk/aboutus/whatwedo/",
                        "target": "_blank",
                    },
                    {
                        "text": "Contact us",
                        "url": "https://surveys.ons.gov.uk/contact-us/",
                        "target": "_blank",
                    },
                    {
                        "text": "Accessibility",
                        "url": "https://www.ons.gov.uk/help/accessibility/",
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
                        "url": "https://surveys.ons.gov.uk/cookies/",
                        "target": "_blank",
                    },
                    {
                        "text": "Privacy and data protection",
                        "url": "https://surveys.ons.gov.uk/privacy-and-data-protection/",
                        "target": "_blank",
                    },
                ]
            }
        ],
    }
    return {**footer_context, **business}


@fixture
def expected_footer_nisra_theme():
    return {
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


@pytest.fixture()
def session_data():
    return SessionData(
        tx_id="123",
        schema_name="test_checkbox",
        display_address="68 Abingdon Road, Goathill",
        period_str=None,
        language_code="cy",
        launch_language_code="en",
        survey_url=None,
        ru_name=None,
        ru_ref=None,
        submitted_at=datetime.now(timezone.utc).isoformat(),
        response_id="321",
        case_id="789",
    )


@pytest.fixture()
def session_store(session_data):
    store = SessionStore("user_ik", "pepper", "eq_session_id")
    store.session_data = session_data
    return store
