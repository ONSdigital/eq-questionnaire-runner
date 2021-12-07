from typing import Optional, Union
from urllib.parse import urlencode

from flask import g, request

from app.globals import get_session_store
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.utilities.schema import get_allowed_languages

LANGUAGE_TEXT = {
    "en": "English",
    "cy": "Cymraeg",
}


def handle_language():
    session_store = get_session_store()
    if session_store:
        launch_language = (
            session_store.session_data.launch_language_code or DEFAULT_LANGUAGE_CODE
        )
        # pylint: disable=assigning-non-slot
        g.allowed_languages = get_allowed_languages(
            session_store.session_data.schema_name, launch_language
        )
        request_language = request.args.get("language_code")
        if request_language and request_language in g.allowed_languages:
            session_store.session_data.language_code = request_language
            session_store.save()


def get_languages_context(current_language: str) -> Optional[dict[str, list[dict]]]:
    context = []
    allowed_languages = g.get("allowed_languages")
    if allowed_languages and len(allowed_languages) > 1:
        for language in allowed_languages:
            context.append(_get_language_context(language, current_language))
        return {"languages": context}
    return None


def _get_language_context(
    language_code: str, current_language: str
) -> dict[str, Union[str, bool]]:
    return {
        "ISOCode": language_code,
        "url": _get_query_string_with_language(language_code),
        "text": LANGUAGE_TEXT[language_code],
        "current": language_code == current_language,
    }


def _get_query_string_with_language(language_code: str) -> str:
    request_args = dict(request.args.items())
    request_args["language_code"] = language_code
    return f"?{urlencode(request_args)}"
