from app.helpers.template_helpers import (
    get_census_base_url,
    get_contact_us_url,
    get_data_layer,
)


def test_get_contact_us_url_nisra_theme():
    expected = "https://census.gov.uk/ni/contact-us/"
    result = get_contact_us_url("census-nisra", "en")

    assert expected == result


def test_get_contact_us_url_census_en():
    expected = "https://census.gov.uk/contact-us/"
    result = get_contact_us_url("census", "en")

    assert expected == result


def test_get_contact_us_url_census_cy():
    expected = "https://cyfrifiad.gov.uk/cysylltu-a-ni/"
    result = get_contact_us_url("census", "cy")

    assert expected == result


def test_get_data_layer_nisra_theme():
    expected = [{"nisra": True}]
    result = get_data_layer("census-nisra")

    assert expected == result


def test_get_census_base_url():
    expected = "https://census.gov.uk/"
    result = get_census_base_url()

    assert expected == result


def test_get_census_base_url_nisra_theme():
    expected = "https://census.gov.uk/ni/"
    result = get_census_base_url(schema_theme="census-nisra")

    assert expected == result


def test_get_census_base_url_welsh():
    expected = "https://cyfrifiad.gov.uk/"
    result = get_census_base_url(language_code="cy")

    assert expected == result
