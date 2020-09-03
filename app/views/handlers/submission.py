from datetime import datetime

import simplejson as json
from flask import current_app
from flask import session as cookie_session
from sdc.crypto.encrypter import encrypt

from app.globals import get_session_store
from app.keys import KEY_PURPOSE_SUBMISSION
from app.submitter.converter import convert_answers
from app.submitter.submission_failed import SubmissionFailedException


class SubmissionHandler:
    def __init__(self, schema, questionnaire_store, full_routing_path):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._full_routing_path = full_routing_path
        self._session_store = get_session_store()
        self._metadata = questionnaire_store.metadata

    def submit_questionnaire(self):

        payload = self.get_payload()
        message = json.dumps(payload, for_json=True)

        encrypted_message = encrypt(
            message, current_app.eq["key_store"], KEY_PURPOSE_SUBMISSION
        )
        submitted = current_app.eq["submitter"].send_message(
            encrypted_message,
            questionnaire_id=self._metadata.get("questionnaire_id"),
            case_id=self._metadata.get("case_id"),
            tx_id=self._metadata.get("tx_id"),
        )

        if not submitted:
            raise SubmissionFailedException()

        cookie_session["submitted"] = True

        self._store_submitted_time_and_display_address_in_session()
        self._questionnaire_store.delete()

    def get_payload(self):
        payload = convert_answers(
            self._schema, self._questionnaire_store, self._full_routing_path
        )
        payload[
            "submission_language_code"
        ] = self._session_store.session_data.language_code
        return payload

    def _store_submitted_time_and_display_address_in_session(self):
        session_data = self._session_store.session_data
        session_data.display_address = self._metadata.get("display_address")
        session_data.submitted_time = datetime.utcnow().isoformat()
        self._session_store.save()
