from typing import Any, Sequence

from wtforms import TextAreaField

from app.utilities.types import TextAreaValidatorType


class MaxTextAreaField(TextAreaField):
    def __init__(
        self,
        *,
        description: str,
        rows: int,
        maxlength: int,
        validators: Sequence[TextAreaValidatorType],
        label: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            label=label, validators=validators, description=description, **kwargs
        )
        self.rows = rows
        self.maxlength = maxlength
