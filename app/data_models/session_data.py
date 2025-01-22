from typing import Any


class SessionData:
    def __init__(
        self,
        language_code: str | None = None,
        confirmation_email_count: int = 0,
        feedback_count: int = 0,
        **_: Any,
    ):
        self.language_code = language_code
        self.confirmation_email_count = confirmation_email_count
        self.feedback_count = feedback_count
