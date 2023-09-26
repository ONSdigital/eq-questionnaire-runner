from typing import Any, Callable, Sequence

from wtforms import TextAreaField


class MaxTextAreaField(TextAreaField):
    def __init__(
        self,
        *,
        description: str,
        rows: int,
        maxlength: int,
        validators: Sequence[Callable],
        label: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            label=label, validators=validators, description=description, **kwargs
        )
        self.rows = rows
        self.maxlength = maxlength
