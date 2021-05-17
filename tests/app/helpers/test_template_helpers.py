from app.helpers.template_helpers import (
    context_helper_factory,
    get_base_url,
    get_data_layer,
)


def test_footer_context_census_theme(app):
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

        context_helper = context_helper_factory(
            "census-nisra", "en", "https://census.gov.uk/ni/"
        )

        result = context_helper.footer_context()
        assert expected == result


def test_footer_context_nisra_theme(app):
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

        context_helper = context_helper_factory(
            "census-nisra", "en", "https://census.gov.uk/ni/"
        )

        result = context_helper.footer_context()
        assert expected == result


def test_get_static_content_urls_census_nisra():
    base_url = "https://census.gov.uk/ni/"
    context_helper = context_helper_factory("census-nisra", "en", base_url)

    expected = {
        "help": f"{base_url}help/help-with-the-questions/online-questions-help/",
        "cookies": f"{base_url}cookies/",
        "accessibility_statement": f"{base_url}accessibility-statement/",
        "privacy_and_data_protection": f"{base_url}privacy-and-data-protection/",
        "terms_and_conditions": f"{base_url}terms-and-conditions/",
        "contact_us": f"{base_url}contact-us/",
    }

    assert expected == context_helper.static_content_urls


def test_get_static_content_urls_census_en():
    base_url = "https://census.gov.uk/"
    context_helper = context_helper_factory("census", "en", base_url)

    expected = {
        "help": f"{base_url}help/how-to-answer-questions/online-questions-help/",
        "cookies": f"{base_url}cookies/",
        "accessibility_statement": f"{base_url}accessibility-statement/",
        "privacy_and_data_protection": f"{base_url}privacy-and-data-protection/",
        "terms_and_conditions": f"{base_url}terms-and-conditions/",
        "contact_us": f"{base_url}contact-us/",
        "languages": f"{base_url}help/languages-and-accessibility/languages/",
        "bsl_and_audio_videos": f"{base_url}help/languages-and-accessibility/accessibility/accessible-videos-with-bsl/",
    }

    result = context_helper.static_content_urls

    assert expected == result


def test_get_static_content_urls_census_cy():
    base_url = "https://cyfrifiad.gov.uk/"
    context_helper = context_helper_factory("census", "cy", base_url)

    expected = {
        "help": f"{base_url}help/sut-i-ateb-y-cwestiynau/help-y-cwestiynau-ar-lein/",
        "cookies": f"{base_url}cwcis/",
        "accessibility_statement": f"{base_url}datganiad-hygyrchedd/",
        "privacy_and_data_protection": f"{base_url}preifatrwydd-a-diogelu-data/",
        "terms_and_conditions": f"{base_url}telerau-ac-amodau/",
        "contact_us": f"{base_url}cysylltu-a-ni/",
        "languages": f"{base_url}help/ieithoedd-a-hygyrchedd/ieithoedd/",
        "bsl_and_audio_videos": f"{base_url}help/ieithoedd-a-hygyrchedd/hygyrchedd/fideos-hygyrch-gyda-bsl/",
    }
    result = context_helper.static_content_urls

    assert expected == result


def test_get_page_header_context_business():
    expected = {
        "logo": "ons-logo-pos-en",
        "logoAlt": "Office for National Statistics logo",
    }
    context_helper = context_helper_factory("business", "en", "https://ons.gov.uk")
    result = context_helper.page_header_context
    assert result == expected


def test_get_page_header_context_census():
    expected = {
        "census": {
            "logo": "ons-logo-pos-en",
            "logoAlt": "Office for National Statistics logo",
            "titleLogo": "census-logo-en",
            "titleLogoAlt": "Census 2021",
        }
    }
    context_helper = context_helper_factory("census", "en", "https://census.gov.uk")
    result = context_helper.page_header_context
    assert result == expected


def test_get_page_header_context_census_nisra():
    expected = {
        "logo": "nisra-logo-en",
        "logoAlt": "Northern Ireland Statistics and Research Agency logo",
        "titleLogo": "census-logo-en",
        "titleLogoAlt": "Census 2021",
        "customHeaderLogo": "nisra",
        "mobileLogo": "nisra-logo-en-mobile",
    }

    context_helper = context_helper_factory(
        "census-nisra", "en", "https://census.gov.uk"
    )
    result = context_helper.page_header_context
    assert result == expected


def test_get_data_layer_nisra_theme():
    expected = [{"nisra": True}]
    result = get_data_layer("census-nisra")

    assert expected == result


def test_get_base_url():
    expected = "https://census.gov.uk/"
    result = get_base_url(schema_theme="census", language_code="en")

    assert expected == result


def test_get_base_url_nisra_theme():
    expected = "https://census.gov.uk/ni/"
    result = get_base_url(schema_theme="census-nisra", language_code="en")

    assert expected == result


def test_get_base_url_welsh():
    expected = "https://cyfrifiad.gov.uk/"
    result = get_base_url(schema_theme="census", language_code="cy")

    assert expected == result


def test_get_base_url_welsh_is_priority_over_nisra():
    expected = "https://cyfrifiad.gov.uk/"
    result = get_base_url(schema_theme="census-nisra", language_code="cy")

    assert expected == result


def test_get_base_url_ga():
    expected = "https://census.gov.uk/"
    result = get_base_url(schema_theme="census", language_code="ga")

    assert expected == result
