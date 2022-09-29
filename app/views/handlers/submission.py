from datetime import datetime, timezone
from functools import cached_property

from flask import current_app
from flask import session as cookie_session
from sdc.crypto.encrypter import encrypt

from app.globals import get_session_store
from app.keys import KEY_PURPOSE_SUBMISSION
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.submitter.converter import convert_answers
from app.submitter.submission_failed import SubmissionFailedException
from app.utilities.json import json_dumps


class SubmissionHandler:
    def __init__(self, schema, questionnaire_store, full_routing_path):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._full_routing_path = full_routing_path
        self._session_store = get_session_store()
        self._metadata = questionnaire_store.metadata

    @cached_property
    def submitted_at(self):
        return datetime.now(timezone.utc).replace(microsecond=0)

    def submit_questionnaire(self):
        payload = self.get_payload()
        message = json_dumps(payload)

        encrypted_message = encrypt(
            message, current_app.eq["key_store"], KEY_PURPOSE_SUBMISSION
        )
        submitted = current_app.eq["submitter"].send_message(
            encrypted_message,
            case_id=self._metadata["case_id"],
            tx_id=self._metadata.get("tx_id"),
        )

        if not submitted:
            raise SubmissionFailedException()

        cookie_session["submitted"] = True

        self._questionnaire_store.submitted_at = self.submitted_at
        self._questionnaire_store.save()

    def get_payload(self):
        payload = convert_answers(
            self._schema,
            self._questionnaire_store,
            self._full_routing_path,
            self.submitted_at,
        )
        payload["submission_language_code"] = (
            self._session_store.session_data.language_code or DEFAULT_LANGUAGE_CODE
        )
        return payload
