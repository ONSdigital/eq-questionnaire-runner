from babel.plural import PluralRule

from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE


def get_plural_form_key(count: int, language: str = DEFAULT_LANGUAGE_CODE) -> str:
    mappings = {
        "en": {"one": "n is 1"},
        "cy": {
            "zero": "n is 0",
            "one": "n is 1",
            "two": "n is 2",
            "few": "n is 3",
            "many": "n is 6",
        },
        "ga": {
            "one": "n is 1",
            "two": "n is 2",
            "few": "n in 3..6",
            "many": "n in 7..10",
        },
        "eo": {"one": "n is 1"},
    }

    plural_rule = PluralRule(mappings[language])
    plural_form: str = plural_rule(count)

    return plural_form
