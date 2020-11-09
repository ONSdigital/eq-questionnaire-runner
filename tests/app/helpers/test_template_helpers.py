from app.helpers.template_helpers import (
    get_census_base_url,
    get_contact_us_url,
    get_data_layer,
    get_footer_urls,
)


def test_get_contact_us_url_census_nisra():
    base_url = "https://census.gov.uk/ni"
    expected = f"{base_url}contact-us/"
    result = get_contact_us_url("en", base_url)

    assert expected == result


def test_get_contact_us_url_census_en():
    base_url = "https://census.gov.uk/"
    expected = f"{base_url}contact-us/"
    result = get_contact_us_url("en", base_url)

    assert expected == result


def test_get_contact_us_url_census_cy():
    base_url = "https://census.gov.uk/"
    expected = f"{base_url}cysylltu-a-ni/"
    result = get_contact_us_url("cy", base_url)

    assert expected == result


def test_get_footer_urls_nisra_theme():
    expected = {
        "help_path": "help/help-with-the-questions/online-questions-help/",
        "cookies_path": "cookies/",
        "accessibility_statement_path": "accessibility/",
        "privacy_and_data_protection_path": "privacy-and-data-protection/",
        "terms_and_conditions_path": "terms-and-conditions/"
    }

    result = get_footer_urls("en", "census-nisra")

    assert expected == result


def test_get_footer_urls_census_en():
    expected = {
        "help_path": "help/how-to-answer-questions/online-questions-help/",
        "cookies_path": "cookies/",
        "accessibility_statement_path": "accessibility/",
        "privacy_and_data_protection_path": "privacy-and-data-protection/",
        "terms_and_conditions_path": "terms-and-conditions/"
    }

    result = get_footer_urls("en", "census")

    assert expected == result


def test_get_footer_urls_census_cy():
    expected = {
        "help_path": "help/sut-i-ateb-y-cwestiynau/help-y-cwestiynau-ar-lein/",
        "cookies_path": "cwcis/",
        "accessibility_statement_path": "hygyrchedd/",
        "privacy_and_data_protection_path": "preifatrwydd-a-diogelu-data/",
        "terms_and_conditions_path": "telerau-ac-amodau/"
    }
    result = get_footer_urls("cy", "census")

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
