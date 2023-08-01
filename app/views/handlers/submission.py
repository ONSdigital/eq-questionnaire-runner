from datetime import datetime, timezone
from functools import cached_property

from flask import current_app
from flask import session as cookie_session
from sdc.crypto.encrypter import encrypt

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.data_models import QuestionnaireStore
from app.data_models.metadata_proxy import MetadataProxy
from app.globals import get_session_store
from app.keys import KEY_PURPOSE_SUBMISSION
from app.questionnaire.questionnaire_schema import (
    DEFAULT_LANGUAGE_CODE,
    QuestionnaireSchema,
)
from app.questionnaire.routing_path import RoutingPath
from app.submitter.converter import convert_answers
from app.submitter.converter_v2 import convert_answers_v2
from app.submitter.submission_failed import SubmissionFailedException
from app.utilities.json import json_dumps


def get_receipting_metadata(metadata: MetadataProxy) -> dict:
    return (
        {item: metadata[item] for item in metadata.survey_metadata.receipting_keys}
        if (
            metadata.version is AuthPayloadVersion.V2
            and metadata.survey_metadata
            and metadata.survey_metadata.receipting_keys
        )
        else {}
    )


class SubmissionHandler:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        full_routing_path: list[RoutingPath],
    ):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._full_routing_path = full_routing_path
        self._session_store = get_session_store()
        # Type ignore: It isn't possible to not have metadata at this point
        self._metadata: MetadataProxy = questionnaire_store.metadata  # type: ignore

    @cached_property
    def submitted_at(self) -> datetime:
        return datetime.now(timezone.utc).replace(microsecond=0)

    def submit_questionnaire(self) -> None:
        payload = self.get_payload()

        message = json_dumps(payload)

        encrypted_message = encrypt(
            message,
            # Type ignore: current_app can return empty Local Proxy. Similar to other files, this is ignored.
            current_app.eq["key_store"],  # type: ignore
            KEY_PURPOSE_SUBMISSION,
        )

        additional_metadata = get_receipting_metadata(self._metadata)

        # Type ignore: current_app can return empty Local Proxy. Similar to other files, this is ignored.
        submitted = current_app.eq["submitter"].send_message(  # type: ignore
            encrypted_message,
            case_id=self._metadata.case_id,
            tx_id=self._metadata.tx_id,
            **additional_metadata,
        )

        if not submitted:
            raise SubmissionFailedException()

        cookie_session["submitted"] = True

        self._questionnaire_store.submitted_at = self.submitted_at
        self._questionnaire_store.save()

    def get_payload(self) -> dict:
        answer_converter = (
            convert_answers_v2
            if self._metadata.version is AuthPayloadVersion.V2
            else convert_answers
        )

        payload = answer_converter(
            self._schema,
            self._questionnaire_store,
            self._full_routing_path,
            self.submitted_at,
        )

        payload["submission_language_code"] = (
            # Type ignore: session_data will exist by this stage
            self._session_store.session_data.language_code  # type: ignore
            or DEFAULT_LANGUAGE_CODE
        )
        return payload
