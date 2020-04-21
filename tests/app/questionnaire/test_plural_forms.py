from app.questionnaire.plural_forms import get_plural_form_key


def test_lookup_count_key_en():
    assert get_plural_form_key(1) == "one"
    assert get_plural_form_key(0) == "other"
    assert get_plural_form_key(2) == "other"
    assert get_plural_form_key(3) == "other"
    assert get_plural_form_key(4) == "other"
    assert get_plural_form_key(5) == "other"
    assert get_plural_form_key(500) == "other"


def test_lookup_count_key_cy():
    assert get_plural_form_key(0, language="cy") == "zero"
    assert get_plural_form_key(1, language="cy") == "one"
    assert get_plural_form_key(2, language="cy") == "two"
    assert get_plural_form_key(3, language="cy") == "few"
    assert get_plural_form_key(6, language="cy") == "many"
    assert get_plural_form_key(7, language="cy") == "other"
    assert get_plural_form_key(500, language="cy") == "other"
