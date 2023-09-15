from datetime import datetime
from typing import Any, Iterable, Mapping, MutableMapping, OrderedDict

from structlog import get_logger

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.data_models import AnswerStore, ListStore, ProgressStore, QuestionnaireStore
from app.data_models.metadata_proxy import MetadataProxy, NoMetadataException
from app.data_models.supplementary_data_store import SupplementaryDataStore
from app.questionnaire.questionnaire_schema import (
    DEFAULT_LANGUAGE_CODE,
    QuestionnaireSchema,
)
from app.questionnaire.routing_path import RoutingPath
from app.submitter.convert_payload_0_0_1 import convert_answers_to_payload_0_0_1
from app.submitter.convert_payload_0_0_3 import convert_answers_to_payload_0_0_3

logger = get_logger()

MetadataType = Mapping[str, str | list | None]


class DataVersionError(Exception):
    def __init__(self, version: str):
        super().__init__()
        self.version = version

    def __str__(self) -> str:
        return f"Data version {self.version} not supported"


def convert_answers_v2(
    schema: QuestionnaireSchema,
    questionnaire_store: QuestionnaireStore,
    full_routing_path: Iterable[RoutingPath],
    submitted_at: datetime,
    flushed: bool = False,
) -> dict[str, Any]:
    """
    Create the JSON answer format for down stream processing, the format can be found here:
    https://github.com/ONSdigital/ons-schema-definitions/blob/main/docs/eq_runner_to_downstream_payload_v2.md

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

    payload: dict = {
        "case_id": metadata.case_id,
        "tx_id": metadata.tx_id,
        "type": "uk.gov.ons.edc.eq:surveyresponse",
        "version": AuthPayloadVersion.V2.value,
        "data_version": schema.json["data_version"],
        "origin": "uk.gov.ons.edc.eq",
        "collection_exercise_sid": metadata.collection_exercise_sid,
        "schema_name": metadata.schema_name,
        "flushed": flushed,
        "submitted_at": submitted_at.isoformat(),
        "launch_language_code": metadata.language_code or DEFAULT_LANGUAGE_CODE,
    }

    optional_properties = get_optional_payload_properties(metadata, response_metadata)

    payload["survey_metadata"] = {"survey_id": survey_id}
    if metadata.survey_metadata:
        payload["survey_metadata"].update(metadata.survey_metadata.data)

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

    logger.info("converted answer ready for submission")

    return payload | optional_properties


def get_optional_payload_properties(
    metadata: MetadataProxy, response_metadata: MutableMapping
) -> MetadataType:
    payload = {}

    for key in ["channel", "region_code"]:
        if value := metadata[key]:
            payload[key] = value
    if started_at := response_metadata.get("started_at"):
        payload["started_at"] = started_at

    return payload


# pylint: disable=too-many-locals
def get_payload_data(
    answer_store: AnswerStore,
    list_store: ListStore,
    schema: QuestionnaireSchema,
    full_routing_path: Iterable[RoutingPath],
    metadata: MetadataProxy,
    response_metadata: MutableMapping,
    progress_store: ProgressStore,
    supplementary_data_store: SupplementaryDataStore,
) -> OrderedDict | dict[str, list | dict]:
    if schema.json["data_version"] == "0.0.1":
        return convert_answers_to_payload_0_0_1(
            metadata=metadata,
            response_metadata=response_metadata,
            answer_store=answer_store,
            list_store=list_store,
            schema=schema,
            full_routing_path=full_routing_path,
            progress_store=progress_store,
            supplementary_data_store=supplementary_data_store,
        )

    if schema.json["data_version"] == "0.0.3":
        answers = convert_answers_to_payload_0_0_3(
            answer_store=answer_store,
            list_store=list_store,
            schema=schema,
            full_routing_path=full_routing_path,
        )

        lists: list = list_store.serialize()
        for list_ in lists:
            # for any lists that were populated by supplementary data, provide the identifier -> list_item_id mappings
            if mapping := supplementary_data_store.list_mappings.get(list_["name"]):
                list_["supplementary_data_mappings"] = mapping

        data: dict[str, list | dict] = {"answers": answers, "lists": lists}

        if supplementary_data_store.raw_data:
            data["supplementary_data"] = supplementary_data_store.raw_data

        if answer_codes := schema.json.get("answer_codes"):
            answer_ids_to_filter = {answer.answer_id for answer in answers}
            if filtered_answer_codes := get_filtered_answer_codes(
                answer_codes=answer_codes, answer_ids_to_filter=answer_ids_to_filter
            ):
                data["answer_codes"] = filtered_answer_codes

        return data

    raise DataVersionError(schema.json["data_version"])


def get_filtered_answer_codes(
    *, answer_codes: Iterable[dict], answer_ids_to_filter: set[str]
) -> list[dict[str, str]]:
    filtered_answer_codes: list[dict] = []
    filtered_answer_codes.extend(
        answer_code
        for answer_code in answer_codes
        if answer_code["answer_id"] in answer_ids_to_filter
    )
    return filtered_answer_codes
