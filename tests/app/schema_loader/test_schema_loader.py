import pytest

from app.utilities.schema import load_schema_from_name


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "schema_name,language_code",
    (
        ("test_checkbox", None),
        ("test_dates", None),
        ("test_language", None),
        ("test_language", "en"),
        ("test_language", "cy"),
    ),
)
def test_load_schema_from_name(schema_name, language_code):
    assert load_schema_from_name(schema_name, language_code=language_code)


@pytest.mark.usefixtures("app")
def test_load_schema_with_invalid_schema_name():
    with pytest.raises(FileNotFoundError):
        load_schema_from_name("test_0309")
