from flask_login import UserMixin


class User(UserMixin):
    USER_SESSION_ERROR_MESSAGE = "No user_id or user_ik found in session"

    def __init__(self, user_id: str | None, user_ik: str | None) -> None:
        if user_id and user_ik:
            self.user_id = user_id
            self.user_ik = user_ik
        else:
            raise ValueError(self.USER_SESSION_ERROR_MESSAGE)
