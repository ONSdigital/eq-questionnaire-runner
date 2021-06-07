import pytest

from app.helpers import get_base_url
from app.settings import CENSUS_CY_BASE_URL, CENSUS_EN_BASE_URL, CENSUS_NIR_BASE_URL


@pytest.mark.parametrize(
    "schema_theme,language_code,expected",
    [
        ("default", "en", CENSUS_EN_BASE_URL),
        ("default", "cy", CENSUS_EN_BASE_URL),
        ("census", "en", CENSUS_EN_BASE_URL),
        ("census", "cy", CENSUS_CY_BASE_URL),
        ("census-nisra", "en", CENSUS_NIR_BASE_URL),
        ("census-nisra", "cy", CENSUS_NIR_BASE_URL),
    ],
)
def test_get_base_url(schema_theme, language_code, expected):
    result = get_base_url(schema_theme=schema_theme, language_code=language_code)
    assert result == expected
