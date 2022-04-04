from functools import wraps
from typing import Any, Callable

from werkzeug.exceptions import Unauthorized

from app.globals import get_session_store
from app.utilities.schema import load_schema_from_session_data


def with_schema(function: Callable) -> Any:
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
    def wrapped_function(*args: Any, **kwargs: Any) -> Any:
        session_store = get_session_store()
        if not session_store:
            raise Unauthorized

        session_data = session_store.session_data
        schema = load_schema_from_session_data(session_data)
        return function(schema, *args, **kwargs)

    return wrapped_function
