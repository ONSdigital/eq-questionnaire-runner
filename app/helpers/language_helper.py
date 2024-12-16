from urllib.parse import urlencode

from flask import g, request
from flask import session as cookie_session
from flask_login import current_user

from app.data_models.metadata_proxy import MetadataProxy
from app.globals import get_metadata, get_session_store
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.utilities.schema import get_allowed_languages, load_schema_from_metadata

LANGUAGE_TEXT = {
    "en": "English",
    "cy": "Cymraeg",
}


def handle_language(metadata: MetadataProxy | None = None) -> None:
    session_store = get_session_store()

    if session_store and session_store.session_data:
        if not metadata:
            metadata = get_metadata(current_user)

        schema_name = metadata.schema_name if metadata else None
        language_code = metadata.language_code if metadata else None

        launch_language = language_code or DEFAULT_LANGUAGE_CODE
        g.allowed_languages = get_allowed_languages(schema_name, launch_language)
        request_language = request.args.get("language_code")
        if request_language and request_language in g.allowed_languages:
            if metadata:
                schema = load_schema_from_metadata(
                    metadata=metadata, language_code=request_language
                )
                if schema.json["title"] != cookie_session.get("title"):
                    cookie_session["title"] = schema.json["title"]

            cookie_session["language_code"] = request_language
            session_store.session_data.language_code = request_language
            session_store.save()


def get_languages_context(current_language: str) -> dict[str, list[dict]] | None:
    context = []
    allowed_languages = g.get("allowed_languages")
    if allowed_languages and len(allowed_languages) > 1:
        for language in allowed_languages:
            context.append(_get_language_context(language, current_language))
        return {"languages": context}

    if (language := cookie_session.get("language_code")) and language in LANGUAGE_TEXT:
        return {"languages": [_get_language_context(language, language)]}

    return None


def _get_language_context(
    language_code: str, current_language: str
) -> dict[str, str | bool]:
    return {
        "isoCode": language_code,
        "url": _get_query_string_with_language(language_code),
        "text": LANGUAGE_TEXT[language_code],
        "current": language_code == current_language,
    }


def _get_query_string_with_language(language_code: str) -> str:
    request_args = dict(request.args.items())
    request_args["language_code"] = language_code
    return f"?{urlencode(request_args)}"
