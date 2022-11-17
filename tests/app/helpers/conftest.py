from pytest import fixture

from app.helpers.template_helpers import ContextHelper
from app.settings import (
    ACCOUNT_SERVICE_BASE_URL,
    ACCOUNT_SERVICE_BASE_URL_SOCIAL,
    CY_ONS_URL,
    ONS_URL,
)
from app.survey_config.census_config import CY_BASE_URL, EN_BASE_URL


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


def footer_context():
    return {
        "lang": "en",
        "crest": True,
        "newTabWarning": "The following links open in a new tab",
        "copyrightDeclaration": {
            "copyright": "Crown copyright and database rights 2020 OS 100019153.",
            "text": "Use of address data is subject to the terms and conditions.",
        },
    }


def welsh_footer_context():
    return {
        "lang": "cy",
        "crest": True,
        "newTabWarning": "The following links open in a new tab",
        "copyrightDeclaration": {
            "copyright": "Crown copyright and database rights 2020 OS 100019153.",
            "text": "Use of address data is subject to the terms and conditions.",
        },
    }


def expected_footer_census_theme():
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
    return {**footer_context(), **census}


def expected_footer_census_theme_no_cookie():
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
    }
    return {**footer_context(), **census}


def expected_footer_business_theme():
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
    return {**footer_context(), **business}


def expected_footer_business_theme_no_cookie():
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
                        "text": "Accessibility",
                        "url": "https://www.ons.gov.uk/help/accessibility/",
                        "target": "_blank",
                    },
                ]
            }
        ],
    }
    return {**footer_context(), **business}


def expected_footer_social_theme():
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
                        "url": f"{ONS_URL}/aboutus/contactus/surveyenquiries",
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
    return {**footer_context(), **social}


def expected_footer_welsh_social_theme():
    social = {
        "rows": [
            {
                "itemsList": [
                    {
                        "text": "What we do",
                        "url": f"{CY_ONS_URL}/aboutus/whatwedo/",
                        "target": "_blank",
                    },
                    {
                        "text": "Contact us",
                        "url": f"{CY_ONS_URL}/aboutus/contactus/surveyenquiries",
                        "target": "_blank",
                    },
                    {
                        "text": "Accessibility",
                        "url": f"{CY_ONS_URL}/help/accessibility/",
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
                        "url": f"{ACCOUNT_SERVICE_BASE_URL_SOCIAL}/cy/cookies/",
                        "target": "_blank",
                    },
                    {
                        "text": "Privacy and data protection",
                        "url": f"{ACCOUNT_SERVICE_BASE_URL_SOCIAL}/cy/privacy-and-data-protection/",
                        "target": "_blank",
                    },
                ]
            }
        ],
    }
    return {**welsh_footer_context(), **social}


def expected_footer_social_theme_no_cookie():
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
                        "text": "Accessibility",
                        "url": "https://www.ons.gov.uk/help/accessibility/",
                        "target": "_blank",
                    },
                ]
            }
        ],
    }
    return {**footer_context(), **social}


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


def expected_footer_census_welsh_theme():
    return {
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
                        "url": f"{CY_BASE_URL}/help/sut-i-ateb-y-cwestiynau/help-y-cwestiynau-ar-lein/",
                        "target": "_blank",
                    },
                    {
                        "text": "Contact us",
                        "url": f"{CY_BASE_URL}/cysylltu-a-ni/",
                        "target": "_blank",
                    },
                    {
                        "text": "Languages",
                        "url": f"{CY_BASE_URL}/help/ieithoedd-a-hygyrchedd/ieithoedd/",
                        "target": "_blank",
                    },
                    {
                        "text": "BSL and audio videos",
                        "url": f"{CY_BASE_URL}/help/ieithoedd-a-hygyrchedd/hygyrchedd/fideos-hygyrch-gyda-bsl/",
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
                        "url": f"{CY_BASE_URL}/cwcis/",
                        "target": "_blank",
                    },
                    {
                        "text": "Accessibility statement",
                        "url": f"{CY_BASE_URL}/datganiad-hygyrchedd/",
                        "target": "_blank",
                    },
                    {
                        "text": "Privacy and data protection",
                        "url": f"{CY_BASE_URL}/preifatrwydd-a-diogelu-data/",
                        "target": "_blank",
                    },
                    {
                        "text": "Terms and conditions",
                        "url": f"{CY_BASE_URL}/telerau-ac-amodau/",
                        "target": "_blank",
                    },
                ]
            }
        ],
    }
