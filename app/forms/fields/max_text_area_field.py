from typing import Any

from wtforms import TextAreaField


class MaxTextAreaField(TextAreaField):
    def __init__(
        self,
        *,
        rows: int,
        maxlength: int,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.rows = rows
        self.maxlength = maxlength
