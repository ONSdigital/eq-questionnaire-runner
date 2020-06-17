from datetime import datetime
import simplejson as json
from flask import url_for, current_app
from sdc.crypto.encrypter import encrypt
from app.globals import get_session_store
from app.keys import KEY_PURPOSE_SUBMISSION
from app.submitter.converter import convert_answers
from app.submitter.submission_failed import SubmissionFailedException


class SubmissionHandler:
    def __init__(self, schema, questionnaire_store, full_routing_path):
        self.schema = schema
        self.questionnaire_store = questionnaire_store
        self.full_routing_path = full_routing_path

    def submit_message(self):
        message = json.dumps(
            convert_answers(
                self.schema, self.questionnaire_store, self.full_routing_path
            ),
            for_json=True,
        )
        encrypted_message = encrypt(
            message, current_app.eq["key_store"], KEY_PURPOSE_SUBMISSION
        )
        metadata = self.questionnaire_store.metadata
        submitted = current_app.eq["submitter"].send_message(
            encrypted_message,
            questionnaire_id=metadata.get("questionnaire_id"),
            case_id=metadata.get("case_id"),
            tx_id=metadata.get("tx_id"),
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
