from app.helpers.template_helper import get_contact_us_url


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
