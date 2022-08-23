from typing import Optional


class SessionData:
    def __init__(
        self,
        language_code: Optional[str] = None,
        confirmation_email_count: int = 0,
        feedback_count: int = 0,
    ):
        self.language_code = language_code
        self.confirmation_email_count = confirmation_email_count
        self.feedback_count = feedback_count

    def __len__(self) -> int:
        return len(
            [self.language_code, self.confirmation_email_count, self.feedback_count]
        )
