from datetime import datetime
from typing import Any, Iterable, Mapping, MutableMapping, Optional, Union

from structlog import get_logger

from app.data_models import QuestionnaireStore
from app.data_models.metadata_proxy import MetadataProxy, NoMetadataException
from app.questionnaire.questionnaire_schema import (
    DEFAULT_LANGUAGE_CODE,
    QuestionnaireSchema,
)
from app.questionnaire.routing_path import RoutingPath
from app.submitter.converter_v2 import get_payload_data

logger = get_logger()

MetadataType = Mapping[str, Optional[Union[str, list]]]


def convert_answers(
    schema: QuestionnaireSchema,
    questionnaire_store: QuestionnaireStore,
    full_routing_path: Iterable[RoutingPath],
    submitted_at: datetime,
    flushed: bool = False,
) -> dict[str, Any]:
    """
    Create the JSON answer format for down stream processing in the following format:
    ```
      {
        'tx_id': '0f534ffc-9442-414c-b39f-a756b4adc6cb',
        'type' : 'uk.gov.ons.edc.eq:surveyresponse',
        'version' : '0.0.1',
        'origin' : 'uk.gov.ons.edc.eq',
        'survey_id': '021',
        'flushed': true|false
        'collection':{
          'exercise_sid': 'hfjdskf',
          'schema_name': 'yui789',
          'period': '2016-02-01'
        },
        'started_at': '2016-03-06T15:28:05Z',
        'submitted_at': '2016-03-07T15:28:05Z',
        'launch_language_code': 'en',
        'channel': 'RH',
        'metadata': {
          'user_id': '789473423',
          'ru_ref': '432423423423'
        },
        'data': [
            ...
        ],
      }
    ```

    Args:
        schema: QuestionnaireSchema instance with populated schema json
        questionnaire_store: EncryptedQuestionnaireStorage instance for accessing current questionnaire data
        full_routing_path: The full routing path followed by the user when answering the questionnaire
        submitted_at: The date and time of submission
        flushed: True when system submits the users answers, False when submitted by user.
    Returns:
        Data payload
    """
    metadata = questionnaire_store.metadata
    if not metadata:
        raise NoMetadataException

    response_metadata = questionnaire_store.response_metadata
    answer_store = questionnaire_store.answer_store
    list_store = questionnaire_store.list_store
    progress_store = questionnaire_store.progress_store
    supplementary_data_store = questionnaire_store.supplementary_data_store

    survey_id = schema.json["survey_id"]

    payload = {
        "case_id": metadata.case_id,
        "tx_id": metadata.tx_id,
        "type": "uk.gov.ons.edc.eq:surveyresponse",
        "version": schema.json["data_version"],
        "origin": "uk.gov.ons.edc.eq",
        "survey_id": survey_id,
        "flushed": flushed,
        "submitted_at": submitted_at.isoformat(),
        "collection": build_collection(metadata),
        "metadata": build_metadata(metadata),
        "launch_language_code": metadata.language_code or DEFAULT_LANGUAGE_CODE,
    }

    optional_properties = get_optional_payload_properties(metadata, response_metadata)

    payload["data"] = get_payload_data(
        answer_store=answer_store,
        list_store=list_store,
        schema=schema,
        full_routing_path=full_routing_path,
        metadata=metadata,
        response_metadata=response_metadata,
        progress_store=progress_store,
        supplementary_data_store=supplementary_data_store,
    )

    return payload | optional_properties


def build_collection(metadata: MetadataProxy) -> MetadataType:
    collection_metadata = {
        "exercise_sid": metadata.collection_exercise_sid,
        "schema_name": metadata.schema_name,
        "period": metadata["period_id"],
    }

    if form_type := metadata["form_type"]:
        collection_metadata["instrument_id"] = form_type

    return collection_metadata


def build_metadata(metadata: MetadataProxy) -> MetadataType:
    downstream_metadata = {
        "user_id": metadata["user_id"],
        "ru_ref": metadata["ru_ref"],
    }

    if ref_p_start_date := metadata["ref_p_start_date"]:
        downstream_metadata["ref_period_start_date"] = ref_p_start_date
    if ref_p_end_date := metadata["ref_p_end_date"]:
        downstream_metadata["ref_period_end_date"] = ref_p_end_date
    if display_address := metadata["display_address"]:
        downstream_metadata["display_address"] = display_address

    return downstream_metadata


def get_optional_payload_properties(
    metadata: MetadataProxy, response_metadata: MutableMapping
) -> MetadataType:
    payload = {}

    for key in ["channel", "case_type", "form_type", "region_code", "case_ref"]:
        if value := metadata[key]:
            payload[key] = value
    if started_at := response_metadata.get("started_at"):
        payload["started_at"] = started_at

    return payload
