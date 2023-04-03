from typing import Mapping, Optional

from app.data_models import Answer, ListStore
from app.data_models.answer_store import AnswerStore
from app.data_models.relationship_store import RelationshipStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.relationship_router import RelationshipRouter
from app.questionnaire.routing_path import RoutingPath


# pylint: disable=too-many-locals
def convert_answers_to_payload_0_0_3(
    *,
    answer_store: AnswerStore,
    list_store: ListStore,
    schema: QuestionnaireSchema,
    full_routing_path: RoutingPath,
) -> list[Answer]:
    """
    Convert answers into the data format below
    'data': [
        {
            'value': 'Joe',
            'answer_id': 'first-name',
            'list_item_id': 'axkkdh'
        },
        {
            'value': 'Dimaggio',
            'answer_id': 'last-name',
            'list_item_id': 'axkkdh'
        },
        {
            'value': 'No',
            'answer_id': 'do-you-live-here'
        }
    ]

    For list answers, this method will query the list store and get all answers from the
    add list item block. If there are multiple list collectors for one list, they will have
    the same answer_ids, and will not be duplicated.

    Returns:
        A list of answer dictionaries.
    """
    answers_payload = AnswerStore()

    for routing_path in full_routing_path:
        for block_id in routing_path:
            if block := schema.get_block(block_id):
                block_type = block["type"]
                if block_type == "RelationshipCollector" and "unrelated_block" in block:
                    add_relationships_unrelated_answers(
                        answer_store=answer_store,
                        list_store=list_store,
                        schema=schema,
                        section_id=routing_path.section_id,
                        relationships_block=block,
                        answers_payload=answers_payload,
                    )

                if schema.is_list_block_type(
                    block_type
                ) or schema.is_primary_person_block_type(block_type):
                    add_list_collector_answers(
                        answer_store=answer_store,
                        list_store=list_store,
                        schema=schema,
                        list_collector_block=block,
                        answers_payload=answers_payload,
                    )
                if (question := block.get("question")) and (
                    question.get("dynamic_answers")
                ):
                    resolve_dynamic_answers(
                        question, answer_store, answers_payload, list_store
                    )

                answer_ids = schema.get_answer_ids_for_block(block_id)
                answers_in_block = answer_store.get_answers_by_answer_id(
                    answer_ids, list_item_id=routing_path.list_item_id
                )
                for answer_in_block in answers_in_block:
                    answers_payload.add_or_update(answer_in_block)

    return list(answers_payload.answer_map.values())


def add_list_collector_answers(
    answer_store: AnswerStore,
    list_store: ListStore,
    schema: QuestionnaireSchema,
    list_collector_block: Mapping,
    answers_payload: AnswerStore,
) -> None:
    """Add answers from a ListCollector block.
    Output is added to the `answers_payload` argument."""

    answers_ids_in_add_block = schema.get_answer_ids_for_list_items(
        list_collector_block["id"]
    )
    list_name = list_collector_block["for_list"]
    list_item_ids = list_store[list_name].items
    if answers_ids_in_add_block:
        for list_item_id in list_item_ids:
            for answer_id in answers_ids_in_add_block:
                answer = answer_store.get_answer(answer_id, list_item_id)
                if answer:
                    answers_payload.add_or_update(answer)


def add_relationships_unrelated_answers(
    answer_store: AnswerStore,
    list_store: ListStore,
    schema: QuestionnaireSchema,
    section_id: str,
    relationships_block: Mapping,
    answers_payload: AnswerStore,
) -> Optional[RelationshipStore]:
    relationships_answer_id = schema.get_first_answer_id_for_block(
        relationships_block["id"]
    )
    relationships_answer = answer_store.get_answer(relationships_answer_id)
    if not relationships_answer:
        return None

    relationship_store = RelationshipStore(relationships_answer.value)  # type: ignore
    list_name = relationships_block["for_list"]
    unrelated_block = relationships_block["unrelated_block"]
    unrelated_block_id = unrelated_block["id"]
    unrelated_answer_id = schema.get_first_answer_id_for_block(unrelated_block_id)
    unrelated_no_answer_values = schema.get_unrelated_block_no_answer_values(
        unrelated_answer_id
    )

    relationship_router = RelationshipRouter(
        answer_store=answer_store,
        relationship_store=relationship_store,
        section_id=section_id,
        list_name=list_name,
        list_item_ids=list_store[list_name].items,
        relationships_block_id=relationships_block["id"],
        unrelated_block_id=unrelated_block_id,
        unrelated_answer_id=unrelated_answer_id,
        unrelated_no_answer_values=unrelated_no_answer_values,
    )

    for location in relationship_router.path:
        if location.block_id == unrelated_block_id and (
            unrelated_answer := answer_store.get_answer(
                unrelated_answer_id, list_item_id=location.list_item_id
            )
        ):
            answers_payload.add_or_update(unrelated_answer)


def resolve_dynamic_answers(
    block: dict,
    answer_store: AnswerStore,
    answers_payload: AnswerStore,
    list_store: ListStore,
) -> None:
    for answer in block["dynamic_answers"].get("answers"):
        for list_item_id in list_store.get(
            block["dynamic_answers"]["values"].get("identifier")
        ).items:
            extracted_answer = answer_store.get_answer(
                answer["id"], list_item_id=list_item_id
            )
            answers_payload.add_or_update(extracted_answer)  # type: ignore
