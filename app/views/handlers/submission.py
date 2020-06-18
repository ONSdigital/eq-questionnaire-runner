from datetime import datetime
from flask import url_for, current_app
from sdc.crypto.encrypter import encrypt
from app.globals import get_session_store
from app.keys import KEY_PURPOSE_SUBMISSION
from app.submitter.submission_failed import SubmissionFailedException


class SubmissionHandler:
    def __init__(self, metadata):
        self.metadata = metadata

    def submit_message(self, message):
        encrypted_message = encrypt(
            message, current_app.eq["key_store"], KEY_PURPOSE_SUBMISSION
        )

        submitted = current_app.eq["submitter"].send_message(
            encrypted_message,
            questionnaire_id=self.metadata.get("questionnaire_id"),
            case_id=self.metadata.get("case_id"),
            tx_id=self.metadata.get("tx_id"),
        )

        if not submitted:
            raise SubmissionFailedException()

        self._store_submitted_time_in_session()

    @staticmethod
    def get_next_location_url():
        return url_for("post_submission.get_thank_you")

    @staticmethod
    def _store_submitted_time_in_session():
        session_store = get_session_store()
        session_data = session_store.session_data
        session_data.submitted_time = datetime.utcnow().isoformat()
        session_store.save()
