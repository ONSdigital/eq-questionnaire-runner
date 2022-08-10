from datetime import datetime
from typing import Any, Mapping, Union

from structlog import get_logger

from app.data_models import QuestionnaireStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire.questionnaire_schema import (
    DEFAULT_LANGUAGE_CODE,
    QuestionnaireSchema,
)
from app.questionnaire.routing_path import RoutingPath
from app.submitter.convert_payload_0_0_1 import convert_answers_to_payload_0_0_1
from app.submitter.convert_payload_0_0_3 import convert_answers_to_payload_0_0_3

logger = get_logger()

MetadataType = Mapping[str, Union[str, int, list, dict]]


class DataVersionError(Exception):
    def __init__(self, version: str):
        super().__init__()
        self.version = version

    def __str__(self) -> str:
        return f"Data version {self.version} not supported"


def convert_answers_v2(
    schema: QuestionnaireSchema,
    questionnaire_store: QuestionnaireStore,
    routing_path: RoutingPath,
    submitted_at: datetime,
    flushed: bool = False,
) -> dict[str, Any]:
    """
    Create the JSON answer format for down stream processing in the following format:
    ```
      {
        'tx_id': '0f534ffc-9442-414c-b39f-a756b4adc6cb',
        'type' : 'uk.gov.ons.edc.eq:surveyresponse',
        'version' : {
            'version': 'v2',
            'data_version': '0.0.1',
        },
        'origin' : 'uk.gov.ons.edc.eq',
        'survey_id': '021',
        'flushed': true|false
        'collection_exercise_sid': 'hfjdskf',
        'schema_name': 'yui789',
        'started_at': '2016-03-06T15:28:05Z',
        'submitted_at': '2016-03-07T15:28:05Z',
        'launch_language_code': 'en',
        'channel': 'RH',
        'survey_metadata': {
          'user_id': '789473423',
          'ru_ref': '432423423423',
          'period': '2016-02-01'
        },
        'data': [
            ...
        ],
      }
    ```

    Args:
        schema: QuestionnaireSchema instance with populated schema json
        questionnaire_store: EncryptedQuestionnaireStorage instance for accessing current questionnaire data
        routing_path: The full routing path followed by the user when answering the questionnaire
        submitted_at: The date and time of submission
        flushed: True when system submits the users answers, False when submitted by user.
    Returns:
        Data payload
    """
    metadata = questionnaire_store.metadata
    response_metadata = questionnaire_store.response_metadata
    answer_store = questionnaire_store.answer_store
    list_store = questionnaire_store.list_store

    metadata_proxy = MetadataProxy(metadata)

    survey_id = schema.json["survey_id"]

    payload = {
        "case_id": metadata_proxy.case_id,
        "tx_id": metadata_proxy.tx_id,
        "type": "uk.gov.ons.edc.eq:surveyresponse",
        "version": {
            "data_version": schema.json["data_version"],
            "version": metadata_proxy.version,
        },
        "origin": "uk.gov.ons.edc.eq",
        "collection_exercise_sid": metadata_proxy.collection_exercise_sid,
        "schema_name": metadata_proxy.schema_name,
        "survey_id": survey_id,
        "flushed": flushed,
        "submitted_at": submitted_at.isoformat(),
        "survey_metadata": metadata["survey_metadata"]["data"],
        "launch_language_code": metadata_proxy.language_code or DEFAULT_LANGUAGE_CODE,
    }

    optional_survey_metadata_properties = get_optional_survey_metadata_properties(
        metadata
    )
    optional_properties = get_optional_payload_properties(metadata, response_metadata)

    payload["survey_metadata"].update(optional_survey_metadata_properties)

    if schema.json["data_version"] == "0.0.3":
        payload["data"] = {
            "answers": convert_answers_to_payload_0_0_3(
                answer_store, list_store, schema, routing_path
            ),
            "lists": list_store.serialize(),
        }
    elif schema.json["data_version"] == "0.0.1":
        payload["data"] = convert_answers_to_payload_0_0_1(
            metadata, response_metadata, answer_store, list_store, schema, routing_path
        )
    else:
        raise DataVersionError(schema.json["data_version"])

    logger.info("converted answer ready for submission")

    return payload | optional_properties


def get_optional_payload_properties(
    metadata: MetadataType, response_metadata: Mapping
) -> MetadataType:
    payload = {}

    metadata_proxy = MetadataProxy(metadata)

    for key in ["channel", "region_code"]:
        if value := metadata_proxy.get_metadata_value(key):
            payload[key] = value
    if started_at := response_metadata.get("started_at"):
        payload["started_at"] = started_at

    return payload


def get_optional_survey_metadata_properties(metadata: MetadataType) -> MetadataType:
    metadata_proxy = MetadataProxy(metadata)
    survey_metadata = {}

    for key in ["form_type", "case_ref", "case_type"]:
        if value := metadata_proxy.get_metadata_value(key):
            survey_metadata[key] = value

    return survey_metadata
