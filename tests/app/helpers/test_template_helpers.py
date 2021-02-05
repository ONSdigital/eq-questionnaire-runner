from app.helpers.template_helpers import (
    get_census_base_url,
    get_data_layer,
    get_footer_context,
    get_static_content_urls,
)


def test_get_footer_context_nisra_theme(app):
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

        result = get_footer_context(
            "en",
            {
                "help": "https://census.gov.uk/ni/help/help-with-the-questions/online-questions-help/",
                "cookies": "https://census.gov.uk/ni/cookies/",
                "accessibility_statement": "https://census.gov.uk/ni/accessibility-statement/",
                "privacy_and_data_protection": "https://census.gov.uk/ni/privacy-and-data-protection/",
                "terms_and_conditions": "https://census.gov.uk/ni/terms-and-conditions/",
                "contact_us": "https://census.gov.uk/ni/contact-us/",
            },
            "/sign-out",
            "census-nisra",
        )

        assert expected == result


def test_get_footer_urls_nisra_theme():
    base_url = "https://census.gov.uk/ni/"

    expected = {
        "help": f"{base_url}help/help-with-the-questions/online-questions-help/",
        "cookies": f"{base_url}cookies/",
        "accessibility_statement": f"{base_url}accessibility-statement/",
        "privacy_and_data_protection": f"{base_url}privacy-and-data-protection/",
        "terms_and_conditions": f"{base_url}terms-and-conditions/",
        "contact_us": f"{base_url}contact-us/",
    }

    result = get_static_content_urls("en", base_url, "census-nisra")

    assert expected == result


def test_get_footer_urls_census_en():
    base_url = "https://census.gov.uk/"

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

    result = get_static_content_urls("en", base_url, "census")

    assert expected == result


def test_get_footer_urls_census_cy():
    base_url = "https://cyfrifiad.gov.uk/"

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
    result = get_static_content_urls("cy", base_url, "census")

    assert expected == result


def test_get_data_layer_nisra_theme():
    expected = [{"nisra": True}]
    result = get_data_layer("census-nisra")

    assert expected == result


def test_get_census_base_url():
    expected = "https://census.gov.uk/"
    result = get_census_base_url(schema_theme="census", language_code="en")

    assert expected == result


def test_get_census_base_url_nisra_theme():
    expected = "https://census.gov.uk/ni/"
    result = get_census_base_url(schema_theme="census-nisra", language_code="en")

    assert expected == result


def test_get_census_base_url_welsh():
    expected = "https://cyfrifiad.gov.uk/"
    result = get_census_base_url(schema_theme="census", language_code="cy")

    assert expected == result


def test_get_census_base_url_welsh_is_priority_over_nisra():
    expected = "https://cyfrifiad.gov.uk/"
    result = get_census_base_url(schema_theme="census-nisra", language_code="cy")

    assert expected == result


def test_get_census_base_url_ga():
    expected = "https://census.gov.uk/"
    result = get_census_base_url(schema_theme="census", language_code="ga")

    assert expected == result
