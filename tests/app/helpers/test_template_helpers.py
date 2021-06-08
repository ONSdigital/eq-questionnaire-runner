from app.helpers.template_helpers import ContextHelper, get_survey_config


def test_footer_context_census_theme(app):
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

        survey_config = get_survey_config(
            theme="census",
            language="en",
        )

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["footer"]

    assert result == expected


def test_footer_context_census_nisra_theme(app):
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

        survey_config = get_survey_config(
            theme="census-nisra",
            language="en",
        )

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["footer"]

    assert result == expected


def test_get_page_header_context_business(app):
    expected = {
        "logo": "ons-logo-pos-en",
        "logoAlt": "Office for National Statistics logo",
    }

    with app.app_context():
        survey_config = get_survey_config(
            theme="business",
            language="en",
        )

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["page_header"]

    assert result == expected


def test_get_page_header_context_census(app):
    expected = {
        "logo": "ons-logo-pos-en",
        "logoAlt": "Office for National Statistics logo",
        "titleLogo": "census-logo-en",
        "titleLogoAlt": "Census 2021",
    }

    with app.app_context():
        survey_config = get_survey_config(
            theme="census",
            language="en",
        )

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["page_header"]

    assert result == expected


def test_get_page_header_context_census_nisra(app):
    expected = {
        "logo": "nisra-logo-en",
        "logoAlt": "Northern Ireland Statistics and Research Agency logo",
        "titleLogo": "census-logo-en",
        "titleLogoAlt": "Census 2021",
        "customHeaderLogo": "nisra",
        "mobileLogo": "nisra-logo-en-mobile",
    }

    with app.app_context():
        survey_config = get_survey_config(
            theme="census-nisra",
            language="en",
        )

        result = ContextHelper(
            language="en",
            is_post_submission=False,
            include_csrf_token=True,
            survey_config=survey_config,
        ).context["page_header"]
    assert result == expected
