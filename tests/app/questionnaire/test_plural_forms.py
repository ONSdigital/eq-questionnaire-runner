import pytest

from app.questionnaire.plural_forms import DEFAULT_LANGUAGE_CODE, get_plural_form_key


@pytest.mark.parametrize(
    "count,language,expected",
    (
        (1, DEFAULT_LANGUAGE_CODE, "one"),
        (0, DEFAULT_LANGUAGE_CODE, "other"),
        (2, DEFAULT_LANGUAGE_CODE, "other"),
        (3, DEFAULT_LANGUAGE_CODE, "other"),
        (4, DEFAULT_LANGUAGE_CODE, "other"),
        (5, DEFAULT_LANGUAGE_CODE, "other"),
        (500, DEFAULT_LANGUAGE_CODE, "other"),
        (0, "cy", "zero"),
        (1, "cy", "one"),
        (2, "cy", "two"),
        (3, "cy", "few"),
        (6, "cy", "many"),
        (7, "cy", "other"),
        (500, "cy", "other"),
    ),
)
def test_lookup_count_key(count, language, expected):
    assert get_plural_form_key(count, language=language) == expected
