from pytest import fixture

from app.helpers.template_helpers import ContextHelper
from app.settings import ACCOUNT_SERVICE_BASE_URL, ACCOUNT_SERVICE_BASE_URL_SOCIAL
from app.survey_config.census_config import EN_BASE_URL


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
                        "url": f"{EN_BASE_URL}/help/how-to-answer-questions/online-questions-help/",
                        "target": "_blank",
                    },
                    {
                        "text": "Contact us",
                        "url": f"{EN_BASE_URL}/contact-us/",
                        "target": "_blank",
                    },
                    {
                        "text": "Languages",
                        "url": f"{EN_BASE_URL}/help/languages-and-accessibility/languages/",
                        "target": "_blank",
                    },
                    {
                        "text": "BSL and audio videos",
                        "url": f"{EN_BASE_URL}/help/languages-and-accessibility/accessibility/accessible-videos-with-bsl/",
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
                        "url": f"{EN_BASE_URL}/cookies/",
                        "target": "_blank",
                    },
                    {
                        "text": "Accessibility statement",
                        "url": f"{EN_BASE_URL}/accessibility-statement/",
                        "target": "_blank",
                    },
                    {
                        "text": "Privacy and data protection",
                        "url": f"{EN_BASE_URL}/privacy-and-data-protection/",
                        "target": "_blank",
                    },
                    {
                        "text": "Terms and conditions",
                        "url": f"{EN_BASE_URL}/terms-and-conditions/",
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
                        "url": f"{ACCOUNT_SERVICE_BASE_URL}/contact-us/",
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
                        "url": f"{ACCOUNT_SERVICE_BASE_URL}/cookies/",
                        "target": "_blank",
                    },
                    {
                        "text": "Privacy and data protection",
                        "url": f"{ACCOUNT_SERVICE_BASE_URL}/privacy-and-data-protection/",
                        "target": "_blank",
                    },
                ]
            }
        ],
    }
    return {**footer_context, **business}


@fixture
def expected_footer_social_theme(footer_context):
    social = {
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
                        "url": f"{ACCOUNT_SERVICE_BASE_URL_SOCIAL}/contact-us/",
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
                        "url": f"{ACCOUNT_SERVICE_BASE_URL_SOCIAL}/cookies/",
                        "target": "_blank",
                    },
                    {
                        "text": "Privacy and data protection",
                        "url": f"{ACCOUNT_SERVICE_BASE_URL_SOCIAL}/privacy-and-data-protection/",
                        "target": "_blank",
                    },
                ]
            }
        ],
    }
    return {**footer_context, **social}


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
                        "url": f"{EN_BASE_URL}/ni/help/help-with-the-questions/online-questions-help/",
                        "target": "_blank",
                    },
                    {
                        "text": "Contact us",
                        "url": f"{EN_BASE_URL}/ni/contact-us/",
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
                        "url": f"{EN_BASE_URL}/ni/cookies/",
                        "target": "_blank",
                    },
                    {
                        "text": "Accessibility statement",
                        "url": f"{EN_BASE_URL}/ni/accessibility-statement/",
                        "target": "_blank",
                    },
                    {
                        "text": "Privacy and data protection",
                        "url": f"{EN_BASE_URL}/ni/privacy-and-data-protection/",
                        "target": "_blank",
                    },
                    {
                        "text": "Terms and conditions",
                        "url": f"{EN_BASE_URL}/ni/terms-and-conditions/",
                        "target": "_blank",
                    },
                ]
            }
        ],
        "poweredBy": {
            "logo": "nisra-logo",
            "alt": "NISRA - Northern Ireland Statistics and Research Agency",
        },
    }
