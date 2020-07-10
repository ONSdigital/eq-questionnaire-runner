from datetime import datetime
import simplejson as json
from flask import current_app
from sdc.crypto.encrypter import encrypt
from app.submitter.converter import convert_answers
from app.keys import KEY_PURPOSE_SUBMISSION
from app.submitter.submission_failed import SubmissionFailedException
from app.globals import get_session_store


class SubmissionHandler:
    def __init__(self, schema, questionnaire_store, full_routing_path):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._full_routing_path = full_routing_path
        self.session_store = get_session_store()

    def submit_questionnaire(self):
        message = json.dumps(
            convert_answers(
                self._schema, self._questionnaire_store, self._full_routing_path
            ),
            for_json=True,
        )

        encrypted_message = encrypt(
            message, current_app.eq["key_store"], KEY_PURPOSE_SUBMISSION
        )
        metadata = self._questionnaire_store.metadata
        submitted = current_app.eq["submitter"].send_message(
            encrypted_message,
            questionnaire_id=metadata.get("questionnaire_id"),
            case_id=metadata.get("case_id"),
            tx_id=metadata.get("tx_id"),
        )

        if not submitted:
            raise SubmissionFailedException()

        self._store_submitted_time_in_session()
        self._questionnaire_store.delete()

    def _store_submitted_time_in_session(self):
        session_data = self.session_store.session_data
        session_data.submitted_time = datetime.utcnow().isoformat()
        self.session_store.save()
