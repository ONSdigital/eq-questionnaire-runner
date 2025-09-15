from functools import wraps
from typing import Callable, Concatenate

from flask_login import current_user
from werkzeug.exceptions import Unauthorized

from app.globals import get_metadata, get_session_store
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.schema import load_schema_from_metadata


def with_schema[**P, T](
    function: Callable[Concatenate[QuestionnaireSchema, P], T],
) -> Callable[P, T]:
    """Adds the survey schema as the first argument to the function being wrapped.
    Use on flask request handlers or methods called by flask request handlers.

    May error unless there is a `current_user`, so should be used as follows e.g.

    ```python
    @login_required
    @with_schema
    def get_block(routing_path, schema, *args):
        ...
    ```
    """

    @wraps(function)
    def wrapped_function(*args: P.args, **kwargs: P.kwargs) -> T:
        session_store = get_session_store()
        if (
            not session_store
            or not session_store.session_data
            or not (metadata := get_metadata(current_user))
        ):
            raise Unauthorized

        language_code = session_store.session_data.language_code

        schema = load_schema_from_metadata(
            metadata=metadata, language_code=language_code
        )
        return function(schema, *args, **kwargs)

    return wrapped_function
