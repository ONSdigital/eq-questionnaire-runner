from pytest import fixture

from app.helpers.template_helpers import ContextHelper
from app.settings import ACCOUNT_SERVICE_BASE_URL, ACCOUNT_SERVICE_BASE_URL_SOCIAL
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
    return {**footer_context(), **social}


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
        "poweredBy": ('<svg class="ons-svg-logo ons-svg-logo--nisra" '
               'xmlns="http://www.w3.org/2000/svg" width="170" height="56" '
               'viewBox="0 1 170 54" aria-labelledby="nisra-logo-en-alt">'
               '    <title id="nisra-logo-en-alt">Northern Ireland Statistics '
               'and Research Agency logo</title>'
               '    <g class="ons-svg-logo__group" fill="#222">'
               '        <path '
               'd="M0,39.3c2.7,4.7,6.1,8.1,10.8,10.8c4.6,2.7,9.7,4,14.7,4c7,0,13.8-2.5,19.2-7.1c0.3-0.3,0.6-0.5,0.9-0.8 '
               'c2.1-2,3.9-4.2,5.5-6.9l-15.2-8.8l-1.2-0.7l-8.6-4.9l-0.6-0.4L25,24.8L6.4,35.6l-1.1,0.6L0,39.3L0,39.3z"/>'
               '    </g>'
               '    <g class="ons-svg-logo__group" fill="#222">'
               '        <path '
               'd="M36.4,7.2c-0.4-0.1-0.8-0.3-1.2-0.4c-2.9-0.9-5.9-1.4-9.1-1.4v18.1l9.1,5.3l1.2,0.7l15.2,8.8l1,0.6l-0.6,1 '
               'c-1.5,2.6-3.3,4.9-5.4,6.9l5,2.9c2.7-4.7,3.9-9.3,3.9-14.7C55.6,22.2,47.6,11.4,36.4,7.2L36.4,7.2z"/>'
               '    </g>'
               '    <g class="ons-svg-logo__group" fill="#222">'
               '        <path '
               'd="M6.2,34.4L25,23.5V4.2h1.2c3.1,0,6.2,0.5,9.1,1.4V0c-5.4,0-10,1.2-14.7,4C9.5,10.3,4.2,22.6,6.2,34.4z"/>'
               '    </g>'
               '    <g class="ons-svg-logo__group ons-svg-logo__group--text" '
               'fill="#222">'
               '        <path '
               'd="M94.5,48.4l-1-0.2c-0.4-0.1-0.7-0.2-0.7-0.5s0.3-0.5,0.8-0.5c0.7,0,0.8,0.4,0.8,0.5l0.9-0.2c-0.3-0.9-1.2-1.1-1.8-1.1 '
               'c-1.5,0-1.7,1-1.7,1.5c0,1.1,1,1.3,1.4,1.3l0.8,0.2c0.2,0,0.5,0.2,0.5,0.5c0,0.5-0.7,0.6-1,0.6c-0.7,0-0.9-0.3-1-0.6l-0.8,0.2 '
               'c0.2,0.7,0.9,1.1,1.9,1.1c0.6,0,2-0.2,2-1.5C95.6,49,95.2,48.5,94.5,48.4z '
               'M91.2,49c0-1.3-0.6-2.5-2.1-2.5c-1.3,0-2.1,1-2.1,2.4 '
               'c0,1.1,0.6,2.4,2.1,2.4c0.9,0,1.7-0.4,2-1.4l-0.9-0.2c-0.1,0.2-0.3,0.7-1,0.7c-0.4,0-0.7-0.1-0.9-0.4c-0.3-0.4-0.2-0.7-0.2-1H91.2z '
               'M88.3,47.7c0.2-0.3,0.5-0.4,0.8-0.4c0.4,0,0.6,0.2,0.8,0.4c0.2,0.3,0.2,0.5,0.2,0.7h-2C88.1,48.2,88.2,48,88.3,47.7z '
               'M148.6,49.6l-1.1-3h-1.1l1.6,4.3l0.1,0.3c0,0.1-0.1,0.5-0.3,0.7c-0.2,0.2-0.4,0.1-1,0.1v0.8h0.6c0.4,0,0.9-0.1,1.2-1l1.8-5.2h-0.8L148.6,49.6z '
               'M100.4,49c0-1.3-0.6-2.5-2.1-2.5c-1.3,0-2.1,1-2.1,2.4c0,1.1,0.6,2.4,2.1,2.4c0.9,0,1.7-0.4,2-1.4l-0.9-0.2c-0.1,0.2-0.3,0.7-1,0.7c-0.4,0-0.7-0.1-0.9-0.4c-0.3-0.4-0.2-0.7-0.2-1H100.4z '
               'M97.5,47.7c0.2-0.3,0.5-0.4,0.8-0.4c0.4,0,0.6,0.2,0.8,0.4c0.2,0.3,0.2,0.5,0.2,0.7h-2C97.3,48.2,97.4,48,97.5,47.7z '
               'M144.4,47.4c0.4,0,0.8,0.2,0.8,0.9l0.9-0.1c-0.1-0.4-0.3-1.6-1.8-1.6c-1.3,0-2,1.1-2,2.4c0,1,0.5,2.4,1.9,2.4c1.5,0,1.8-1.3,1.9-1.7l-0.9-0.2c-0.1,0.5-0.4,0.9-0.9,0.9c-0.9,0-0.9-1.2-0.9-1.4s0-0.6,0.1-0.9C143.6,47.9,143.8,47.4,144.4,47.4z '
               'M67.1,48.2L67.1,48.2c-0.1-0.6-0.1-0.9-0.6-1.3c-0.3-0.3-0.9-0.3-1.4-0.3c-0.9,0-1.9,0.3-2.1,1.3l1,0.1c0-0.2,0.2-0.7,1.1-0.7c0.5,0,1,0.1,1,0.7v0.3c-1,0-3.1,0-3.1,1.6c0,0.7,0.5,1.4,1.5,1.4c1.1,0,1.4-0.7,1.5-1c0,0.4,0,0.6,0.2,0.9h1c0-0.2-0.1-0.5-0.1-0.9V48.2z '
               'M64.8,50.5c-0.7,0-0.8-0.5-0.8-0.7c0-0.6,0.5-0.7,0.7-0.8s0.6-0.1,1.2-0.1v0.4H66C66,49.7,65.8,50.5,64.8,50.5z '
               'M76.2,47.2c-0.3-0.7-0.8-0.8-1.2-0.8c-1.4,0-1.8,1.5-1.8,2.4c0,0.5,0.1,2.4,1.7,2.4c0.9,0,1.2-0.7,1.3-1v0.9h1V45h-1V47.2z '
               'M76.1,49.3c0,0.7-0.5,1.2-1,1.2c-0.9,0-0.9-1.2-0.9-1.5c0-0.4,0-1.6,1-1.6c0.2,0,0.5,0.1,0.7,0.3c0.2,0.3,0.2,0.4,0.2,0.8V49.3z '
               'M70.5,46.6c-0.9,0-1.2,0.8-1.4,1.1v-1.1h-0.9v4.6h1.1v-2.1c0-1.6,0.8-1.6,1-1.6c0.2,0,0.7,0,0.7,1.1v2.7h1v-2.7C72,48,72,46.6,70.5,46.6zM105.3,48.2c0-0.6,0-0.9-0.5-1.3c-0.3-0.3-0.9-0.3-1.4-0.3c-0.9,0-1.9,0.3-2.1,1.3l0.9,0.1c0-0.2,0.2-0.7,1.1-0.7c0.5,0,1,0.1,1,0.7v0.3c-1,0-3.1,0-3.1,1.6c0,0.7,0.5,1.4,1.5,1.4c1.1,0,1.4-0.7,1.5-1c0,0.4,0,0.6,0.2,0.9h1c0-0.2-0.1-0.5-0.1-0.9V48.2z '
               'M103,50.5c-0.7,0-0.8-0.5-0.8-0.7c0-0.6,0.5-0.7,0.7-0.8c0.2-0.1,0.6-0.1,1.2-0.1v0.4h0.1C104.2,49.7,104,50.5,103,50.5z '
               'M86.1,46.9c0-0.6-0.2-1-0.6-1.3C85.2,45.2,84.8,45,84,45h-2.7v6.2h1.1v-2.5H84l1,2.5h1.1L85,48.5C85.3,48.4,86.1,48,86.1,46.9z '
               'M83.8,47.8h-1.4v-1.9h1.5c0.8,0,1.1,0.4,1.1,0.9C85,47.6,84.4,47.8,83.8,47.8z '
               'M130.8,46c-0.2,0.1-0.4,0.4-0.4,0.7c-0.3,0-0.5-0.1-0.9-0.1c-1.6,0-1.9,0.9-1.9,1.4c0,0.6,0.4,0.9,0.6,1c-0.2,0.1-0.7,0.4-0.7,1c0,0.3,0.2,0.5,0.4,0.7c-0.3,0.2-0.7,0.4-0.7,0.9c0,1,1,1.2,2.2,1.2c1.9,0,2.4-0.9,2.4-1.5c0-0.6-0.4-1.2-1.6-1.2H129c-0.6,0-0.7-0.3-0.7-0.5c0-0.3,0.2-0.4,0.3-0.4c0.3,0.1,0.5,0.1,0.9,0.1c1.1,0,1.9-0.6,1.9-1.4c0-0.5-0.3-0.8-0.5-1c0.1-0.3,0.3-0.4,0.7-0.4h0.3v-0.7h-0.4C131.2,45.8,131,45.9,130.8,46z '
               'M128.4,50.9c0.3,0.1,0.8,0.1,1.1,0.1h0.7c0.3,0,0.7,0.1,0.7,0.5c0,0.5-0.7,0.6-1.2,0.6c-0.2,0-0.5,0-0.9-0.1c-0.3-0.1-0.6-0.4-0.6-0.7C128.2,51.2,128.3,51.1,128.4,50.9zM130,48.5c-0.1,0.1-0.4,0.2-0.6,0.2c-0.6,0-0.8-0.4-0.8-0.7s0.2-0.8,0.9-0.8s0.8,0.4,0.8,0.7C130.3,48.1,130.3,48.3,130,48.5zM136.5,49c0-1.3-0.6-2.5-2.1-2.5c-1.3,0-2.1,1-2.1,2.4c0,1.1,0.6,2.4,2.1,2.4c0.9,0,1.7-0.4,2-1.4l-0.9-0.2c-0.1,0.2-0.3,0.7-1,0.7c-0.4,0-0.7-0.1-0.9-0.4c-0.3-0.4-0.2-0.7-0.2-1H136.5z '
               'M133.3,48.4c0-0.2,0.1-0.4,0.2-0.7c0.2-0.3,0.5-0.4,0.8-0.4c0.3,0,0.6,0.2,0.8,0.4c0.2,0.3,0.2,0.5,0.2,0.7H133.3z '
               'M111.6,47.4c0.4,0,0.8,0.2,0.8,0.9l0.9-0.1c-0.1-0.4-0.3-1.6-1.8-1.6c-1.3,0-2,1.1-2,2.4c0,1,0.5,2.4,1.9,2.4c1.5,0,1.8-1.3,1.9-1.7l-0.9-0.2c-0.1,0.5-0.4,0.9-0.9,0.9c-0.9,0-0.9-1.2-0.9-1.4s0-0.6,0.1-0.9C110.8,47.9,111,47.4,111.6,47.4z '
               'M139.7,46.6c-0.9,0-1.2,0.8-1.4,1.1v-1.1h-0.9v4.6h1.1v-2.1c0-1.6,0.8-1.6,1-1.6s0.7,0,0.7,1.1v2.7h1v-2.7C141.2,48,141.2,46.6,139.7,46.6z '
               'M116.4,46.5c-0.9,0-1.2,0.7-1.3,1V45h-1v6.2h1V49c0-0.5,0-0.8,0.2-1.2c0.1-0.3,0.5-0.5,0.8-0.5c0.7,0,0.7,0.7,0.7,1.1v2.8h1v-2.9C117.8,47,117.4,46.5,116.4,46.5z '
               'M123.4,45l-2.1,6.2h1l0.5-1.5h2.4l0.5,1.5h1.2l-2.1-6.2H123.4z '
               'M123.1,48.8L124,46l0.9,2.8H123.1z '
               'M107.5,47.6v-1.1h-0.9v4.7h1v-1.9c0-0.7,0.2-1.2,0.3-1.4c0.3-0.4,0.7-0.4,1-0.4v-1.1C107.9,46.4,107.6,47.3,107.5,47.6z '
               'M163.7,38.2c0.4,0,0.8,0.2,0.8,0.9l0.9-0.1c-0.1-0.4-0.3-1.6-1.8-1.6c-1.3,0-2,1.1-2,2.4c0,1,0.5,2.4,1.9,2.4c1.5,0,1.8-1.3,1.9-1.7l-0.9-0.2c-0.1,0.5-0.4,0.9-0.9,0.9c-0.9,0-0.9-1.2-0.9-1.4s0-0.6,0.1-0.9C162.9,38.7,163.1,38.2,163.7,38.2z '
               'M159.5,42h1v-4.6h-1V42z '
               'M139.1,41.8c0.2,0.2,0.6,0.4,1,0.4c0.2,0,0.5,0,0.7-0.1v-0.9h-0.4c-0.5,0-0.7-0.1-0.7-0.7v-2.2h0.9v-0.8h-0.9v-1.3l-0.8,0.1l-0.1,1.2h-0.6v0.8h0.6v2.4C138.8,41.2,138.8,41.5,139.1,41.8z '
               'M67.1,40.2c-0.2-0.4-0.4-0.7-0.4-0.7l-2.2-3.6h-1.2V42h0.9v-4.6c0.1,0.1,0.3,0.6,0.3,0.7l2.4,3.9h1v-6.2h-0.8V40.2z '
               'M157.6,40.5v-2.2h0.9v-0.8h-0.9v-1.3l-0.8,0.1l-0.1,1.2H156v0.8h0.6v2.4c0,0.5,0,0.8,0.3,1.1c0.2,0.2,0.6,0.4,1,0.4c0.2,0,0.5,0,0.7-0.1v-0.9h-0.3C157.8,41.2,157.6,41.1,157.6,40.5z '
               'M91,37.4V42h1v-1.8c0-0.7,0.2-1.2,0.3-1.4c0.3-0.4,0.7-0.4,1-0.4v-1.1c-1,0-1.3,0.9-1.4,1.2v-1.1H91z '
               'M129.1,42v-6.2h-1V38c-0.3-0.7-0.8-0.8-1.2-0.8c-1.4,0-1.8,1.5-1.8,2.4c0,0.5,0.1,2.4,1.7,2.4c0.9,0,1.2-0.7,1.3-1v1H129.1z '
               'M127.1,41.3c-0.9,0-0.9-1.2-0.9-1.5c0-0.4,0-1.6,1-1.6c0.2,0,0.5,0.1,0.7,0.3c0.2,0.3,0.2,0.4,0.2,0.8v0.8C128.1,40.8,127.6,41.3,127.1,41.3z '
               'M103.3,42v-6.2h-1.1V42H103.3z '
               'M111.8,39.9c0-1.3-0.6-2.5-2.1-2.5c-1.3,0-2.1,1-2.1,2.4c0,1.1,0.6,2.4,2.1,2.4c0.9,0,1.7-0.4,2-1.4l-0.9-0.2c-0.1,0.2-0.3,0.7-1,0.7c-0.4,0-0.7-0.1-0.9-0.4c-0.3-0.4-0.2-0.7-0.2-1H111.8z '
               'M108.6,39.2c0-0.2,0.1-0.4,0.2-0.7c0.2-0.3,0.5-0.4,0.8-0.4c0.4,0,0.6,0.2,0.8,0.4c0.2,0.3,0.2,0.5,0.2,0.7H108.6z '
               'M74.2,37.4V42h1v-1.8c0-0.7,0.2-1.2,0.3-1.4c0.3-0.4,0.7-0.4,1-0.4v-1.1c-1,0-1.3,0.9-1.4,1.2v-1.1H74.2z '
               'M159.5,36.9h1v-1.1h-1V36.9z M149.8,42h1v-4.6h-1V42z '
               'M146.9,40.7c0,0.5,0,0.8,0.3,1.1c0.2,0.2,0.6,0.4,1,0.4c0.2,0,0.5,0,0.7-0.1v-0.9h-0.4c-0.5,0-0.7-0.1-0.7-0.7v-2.2h0.9v-0.8h-0.9v-1.3l-0.8,0.1l-0.1,1.2h-0.6v0.8h0.6V40.7z '
               'M71.1,37.3c-1.4,0-2.1,1.1-2.1,2.3c0,1,0.6,2.4,2.1,2.4c1.1,0.1,2.1-0.7,2.1-2.3C73.2,38.5,72.5,37.3,71.1,37.3z '
               'M71.1,41.3c-1,0-1-1.3-1-1.5c0-0.7,0.2-1.5,1-1.5c0.8-0.1,1,0.6,1,1.4C72.1,40.2,72,41.3,71.1,41.3z '
               'M144.3,41.1c0,0.4,0,0.6,0.2,0.9h1c0-0.2-0.1-0.5-0.1-0.9V39h0c0-0.6,0-0.9-0.5-1.3c-0.3-0.3-0.9-0.3-1.4-0.3c-0.9,0-1.9,0.3-2.1,1.3l0.9,0.1c0-0.2,0.2-0.7,1.1-0.7c0.5,0,1,0.1,1,0.7v0.3c-1,0-3.1,0-3.1,1.6c0,0.7,0.5,1.4,1.5,1.4C143.9,42.1,144.2,41.4,144.3,41.1z '
               'M142.4,40.6c0-0.6,0.5-0.7,0.7-0.8c0.2-0.1,0.6-0.1,1.2-0.1v0.4h0.1c0,0.4-0.2,1.2-1.2,1.2C142.5,41.3,142.4,40.8,142.4,40.6z '
               'M112.8,42h1v-6.2h-1V42z '
               'M136,38.4l-1-0.3c-0.3-0.1-0.9-0.3-0.9-0.7c0-0.3,0.2-0.8,1.1-0.8s1.1,0.5,1.1,0.7l1.1-0.3c-0.1-0.2-0.1-0.5-0.5-0.8c-0.5-0.4-1.1-0.5-1.7-0.5c-1.2,0-2.2,0.7-2.2,1.8c0,0.8,0.4,1.4,1.3,1.6l1.4,0.4c0.3,0.1,0.8,0.2,0.8,0.8c0,0.3-0.2,0.8-1.2,0.8c-0.2,0-0.5,0-0.8-0.1c-0.6-0.2-0.7-0.6-0.7-0.8l-1.2,0.3c0.1,0.3,0.2,0.7,0.6,1c0.5,0.4,1.2,0.6,1.9,0.6c1.4,0,2.5-0.7,2.5-1.9C137.6,38.9,136.5,38.6,136,38.4z '
               'M118.9,39c0-0.6,0-0.9-0.5-1.3c-0.3-0.3-0.9-0.3-1.4-0.3c-0.9,0-1.9,0.3-2.1,1.3l0.9,0.1c0-0.2,0.2-0.7,1.1-0.7c0.5,0,1,0.1,1,0.7v0.3c-1,0-3.1,0-3.1,1.6c0,0.7,0.5,1.4,1.5,1.4c1.1,0,1.4-0.7,1.5-1c0,0.4,0,0.6,0.2,0.9h1c0-0.2-0.1-0.5-0.1-0.9V39z '
               'M116.7,41.3c-0.7,0-0.8-0.5-0.8-0.7c0-0.6,0.5-0.7,0.7-0.8c0.2-0.1,0.6-0.1,1.2-0.1v0.4h0.1C117.9,40.5,117.7,41.3,116.7,41.3z '
               'M122.2,38.3c0.2,0,0.7,0,0.7,1.1V42h1v-2.7c0-0.6,0-2-1.5-2c-0.9,0-1.2,0.8-1.4,1.1v-1.1h-0.9V42h1.1v-2.1C121.2,38.3,122,38.3,122.2,38.3zM107,37.3c-1,0-1.3,0.9-1.4,1.2v-1.1h-0.9V42h1v-1.8c0-0.7,0.2-1.2,0.3-1.4c0.3-0.4,0.7-0.4,1-0.4V37.3z '
               'M149.8,36.9h1v-1.1h-1V36.9z '
               'M79,40.5v-2.2h0.9v-0.8H79v-1.3l-0.8,0.1L78,37.4h-0.6v0.8H78v2.4c0,0.5,0,0.8,0.3,1.1c0.2,0.2,0.6,0.4,1,0.4c0.2,0,0.5,0,0.7-0.1v-0.8h-0.3C79.2,41.2,79,41.1,79,40.5z '
               'M154.4,39.3l-1-0.2c-0.4-0.1-0.7-0.2-0.7-0.5c0-0.3,0.3-0.5,0.8-0.5c0.7,0,0.8,0.4,0.8,0.5l0.9-0.2c-0.3-0.9-1.2-1.1-1.8-1.1c-1.5,0-1.7,1-1.7,1.5c0,1.1,1,1.3,1.4,1.3l0.8,0.2c0.2,0,0.5,0.2,0.5,0.5c0,0.5-0.7,0.6-1,0.6c-0.7,0-0.9-0.3-1-0.6l-0.8,0.2c0.2,0.7,0.9,1.1,1.9,1.1c0.6,0,2-0.2,2-1.5C155.5,39.9,155.1,39.4,154.4,39.3z '
               'M81.9,39.8c0-0.5,0-0.8,0.2-1.2c0.1-0.3,0.5-0.5,0.8-0.5c0.7,0,0.7,0.7,0.7,1.1V42h1v-2.9c0-1.3-0.4-1.8-1.4-1.8c-0.9,0-1.2,0.7-1.3,1v-2.4h-1V42h1V39.8z '
               'M89.8,40.8l-0.9-0.2c-0.1,0.2-0.3,0.7-1,0.7c-0.4,0-0.7-0.1-0.9-0.4c-0.3-0.4-0.2-0.7-0.2-1h3.1c0-1.3-0.6-2.5-2.1-2.5c-1.3,0-2.1,1-2.1,2.4c0,1.1,0.6,2.4,2.1,2.4C88.7,42.2,89.5,41.8,89.8,40.8z '
               'M87,38.5c0.2-0.3,0.5-0.4,0.8-0.4c0.3,0,0.6,0.2,0.8,0.4c0.2,0.3,0.2,0.5,0.2,0.7h-2C86.8,39,86.9,38.8,87,38.5z '
               'M168.5,39.3l-1-0.2c-0.4-0.1-0.7-0.2-0.7-0.5c0-0.3,0.3-0.5,0.8-0.5c0.7,0,0.8,0.4,0.8,0.5l0.9-0.2c-0.3-0.9-1.2-1.1-1.8-1.1c-1.5,0-1.7,1-1.7,1.5c0,1.1,1,1.3,1.4,1.3l0.8,0.2c0.2,0,0.5,0.2,0.5,0.5c0,0.5-0.7,0.6-1,0.6c-0.7,0-0.9-0.3-1-0.6l-0.8,0.2c0.2,0.7,0.9,1.1,1.9,1.1c0.6,0,2-0.2,2-1.5C169.6,39.9,169.2,39.4,168.5,39.3z '
               'M97,39.4V42h1v-2.7c0-0.6,0-2-1.5-2c-0.9,0-1.2,0.8-1.4,1.1v-1.1h-0.9V42h1.1v-2.1c0-1.6,0.8-1.6,1-1.6C96.5,38.3,97,38.3,97,39.4z '
               'M151.6,24.8H162l2.2,6.5h5.2l-9.1-27.2h-6l-9,27.2h4.2L151.6,24.8z '
               'M156.8,8.8l4,12.1h-8L156.8,8.8z '
               'M108,27.7c-0.9,0-2-0.1-3.4-0.5c-2.4-0.8-2.9-2.5-3.2-3.5l-4.7,1c0.4,1.3,0.9,2.9,2.7,4.4c2.2,1.8,5.1,2.6,8.4,2.6c6.2,0,10.8-3.1,10.8-8.5c0-5.8-4.7-7.1-7-7.7l-4.6-1.1c-1.4-0.4-3.8-1.1-3.8-3.3c0-1.4,0.9-3.4,4.7-3.4c3.9,0,4.7,2.2,5,3.1l4.6-1.2c-0.2-0.9-0.7-2.2-2.3-3.5c-2.1-1.7-4.8-2.4-7.5-2.4c-5.5,0-9.6,3-9.6,8.1c0,3.5,1.9,6.2,5.9,7.3l6.1,1.5c1.2,0.3,3.3,1,3.3,3.5C113.4,25.3,112.5,27.7,108,27.7z '
               'M127.3,20.1h6.9l4.2,11.2h5.2v-0.1l-4.8-12c1.4-0.6,4.9-2.1,4.9-7.2c0-2.8-1.1-4.6-2.4-5.9c-1.7-1.5-3.7-2.1-7.1-2.1h-11.8v27.2h4.9V20.1z '
               'M127.3,8h6.5c3.5,0,4.8,2,4.8,4c0,3.4-2.8,4.2-5.2,4.2h-6.1V8z '
               'M66.9,10.9c0.2,0.5,1.2,2.6,1.5,3L79,31.2h4.5V4.1h-3.9v19.2c-0.9-1.8-1.6-3-1.7-3.2l-9.5-16H63v27.2h3.9V10.9z '
               'M93.9,4.1H89v27.2h4.9V4.1z"/>'
               '    </g>'
               '</svg>',),
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
