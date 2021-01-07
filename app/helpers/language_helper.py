from urllib.parse import urlencode

from flask import g, request
from flask_babel import get_locale

from app.globals import get_session_store
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.utilities.schema import get_allowed_languages

# eo has been used for Ulstér Scotch as there is no language code in the
# CLDR (http://cldr.unicode.org) for it and this is required for survey runner
# to work (http://babel.pocoo.org/en/latest/locale.html).

LANGUAGE_TEXT = {
    "en": "English",
    "cy": "Cymraeg",
    "ga": "Gaeilge",
    "eo": "Ulstér Scotch",
}


def handle_language():
    session_store = get_session_store()
    if session_store:
        launch_language = (
            session_store.session_data.launch_language_code or DEFAULT_LANGUAGE_CODE
        )
        g.allowed_languages = get_allowed_languages(
            session_store.session_data.schema_name, launch_language
        )
        request_language = request.args.get("language_code")
        if request_language and request_language in g.allowed_languages:
            session_store.session_data.language_code = request_language
            session_store.save()


def get_languages_context():
    context = []
    allowed_languages = g.get("allowed_languages")
    if allowed_languages and len(allowed_languages) > 1:
        for language in allowed_languages:
            context.append(_get_language_context(language))
        return {"languages": context}
    return None


def _get_language_context(language_code):
    return {
        "ISOCode": language_code,
        "url": _get_query_string_with_language(language_code),
        "text": LANGUAGE_TEXT.get(language_code),
        "current": language_code == get_locale().language,
    }


def _get_query_string_with_language(language_code):
    request_args = dict(request.args.items())
    request_args["language_code"] = language_code
    return f"?{urlencode(request_args)}"
