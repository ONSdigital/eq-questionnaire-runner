from functools import wraps

from flask_login import current_user

from app.globals import get_questionnaire_store, get_session_store


def with_questionnaire_store(function):
    """Adds the `questionnaire_store` as an argument, where the `current_user` is defined.
    Use on flask request handlers or methods called by flask request handlers.

    May error unless there is a `current_user`."""

    @wraps(function)
    def wrapped_function(*args, **kwargs):
        questionnaire_store = get_questionnaire_store(
            current_user.user_id, current_user.user_ik
        )
        return function(questionnaire_store, *args, **kwargs)

    return wrapped_function


def with_session_store(function):
    """Adds the `session_store` as an argument.
    Use on flask request handlers or methods called by flask request handlers.
    """

    @wraps(function)
    def wrapped_function(*args, **kwargs):
        session_store = get_session_store()
        return function(session_store, *args, **kwargs)

    return wrapped_function
