from typing import Any

from werkzeug.datastructures import ImmutableMultiDict, MultiDict

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import InvalidLocationException, Location
from app.questionnaire.relationship_location import RelationshipLocation
from app.views.handlers.calculation_summary import (
    CalculatedSummary,
    GrandCalculatedSummary,
)
from app.views.handlers.content import Content
from app.views.handlers.list_add_question import ListAddQuestion
from app.views.handlers.list_collector import ListCollector
from app.views.handlers.list_collector_content import ListCollectorContent
from app.views.handlers.list_edit_question import ListEditQuestion
from app.views.handlers.list_remove_question import ListRemoveQuestion
from app.views.handlers.list_repeating_question import ListRepeatingQuestion
from app.views.handlers.primary_person_list_collector import PrimaryPersonListCollector
from app.views.handlers.primary_person_question import PrimaryPersonQuestion
from app.views.handlers.question import Question
from app.views.handlers.relationships import RelationshipCollector, UnrelatedQuestion

BLOCK_MAPPINGS = {
    "Question": Question,
    "ConfirmationQuestion": Question,
    "ListCollectorDrivingQuestion": Question,
    "ListCollector": ListCollector,
    "ListCollectorContent": ListCollectorContent,
    "ListAddQuestion": ListAddQuestion,
    "ListEditQuestion": ListEditQuestion,
    "ListRemoveQuestion": ListRemoveQuestion,
    "ListRepeatingQuestion": ListRepeatingQuestion,
    "PrimaryPersonListCollector": PrimaryPersonListCollector,
    "PrimaryPersonListAddOrEditQuestion": PrimaryPersonQuestion,
    "RelationshipCollector": RelationshipCollector,
    "UnrelatedQuestion": UnrelatedQuestion,
    "Introduction": Content,
    "Interstitial": Content,
    "CalculatedSummary": CalculatedSummary,
    "GrandCalculatedSummary": GrandCalculatedSummary,
}


def get_block_handler(
    schema: QuestionnaireSchema,
    block_id: str,
    list_item_id: str | None,
    questionnaire_store: QuestionnaireStore,
    language: str | None,
    list_name: str | None = None,
    to_list_item_id: str | None = None,
    request_args: MultiDict[str, str] | None = None,
    form_data: ImmutableMultiDict[str, str] | None = None,
) -> Any:
    block = schema.get_block(block_id)

    if not block:
        raise InvalidLocationException(
            f"block id {block_id} is not valid for this schema"
        )

    if schema.is_block_in_repeating_section(block_id=block["id"]) and not all(
        (list_name, list_item_id)
    ):
        raise InvalidLocationException(
            f"block id {block_id} is in a repeating section without valid list_name/list_item_id"
        )

    block_type = block["type"]
    block_class = BLOCK_MAPPINGS.get(block_type)
    if not block_class:
        raise ValueError(f"block type {block_type} is not valid")

    section_id = schema.get_section_id_for_block_id(block_id)

    if to_list_item_id or block_type == "UnrelatedQuestion":
        location = RelationshipLocation(
            # Type ignore: Block is fetched from schema so must have a corresponding section
            section_id=section_id,  # type: ignore
            block_id=block_id,
            list_item_id=list_item_id,
            to_list_item_id=to_list_item_id,
            list_name=list_name,
        )
    else:
        location = Location(
            # Type ignore: Block is fetched from schema so must have a corresponding section
            section_id=section_id,  # type: ignore
            block_id=block_id,
            list_name=list_name,
            list_item_id=list_item_id,
        )

    return block_class(
        schema, questionnaire_store, language, location, request_args, form_data
    )
