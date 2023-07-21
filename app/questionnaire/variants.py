from typing import Mapping, MutableMapping

from werkzeug.datastructures import ImmutableDict

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.progress_store import ProgressStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.utilities.types import LocationType


# Type ignore: validation should ensure the variant exists when this is called
def choose_variant(  # type: ignore
    block: Mapping,
    schema: QuestionnaireSchema,
    metadata: MetadataProxy | None,
    response_metadata: MutableMapping,
    answer_store: AnswerStore,
    list_store: ListStore,
    variants_key: str,
    single_key: str,
    current_location: LocationType,
    progress_store: ProgressStore,
) -> dict:
    if block.get(single_key):
        # Type ignore: the key passed in will be for a dictionary
        return block[single_key]  # type: ignore
    for variant in block.get(variants_key, []):
        when_rules = variant["when"]

        when_rule_evaluator = RuleEvaluator(
            schema,
            answer_store,
            list_store,
            metadata,
            response_metadata,
            location=current_location,
            progress_store=progress_store,
        )

        if when_rule_evaluator.evaluate(when_rules):
            # Type ignore: question/content key is for a dictionary
            return variant[single_key]  # type: ignore


def choose_question_to_display(
    block: ImmutableDict,
    schema: QuestionnaireSchema,
    metadata: MetadataProxy | None,
    response_metadata: MutableMapping,
    answer_store: AnswerStore,
    list_store: ListStore,
    current_location: LocationType,
    progress_store: ProgressStore,
) -> dict:
    return choose_variant(
        block,
        schema,
        metadata,
        response_metadata,
        answer_store,
        list_store,
        variants_key="question_variants",
        single_key="question",
        current_location=current_location,
        progress_store=progress_store,
    )


def choose_content_to_display(
    block: ImmutableDict,
    schema: QuestionnaireSchema,
    metadata: MetadataProxy | None,
    response_metadata: MutableMapping,
    answer_store: AnswerStore,
    list_store: ListStore,
    current_location: LocationType,
    progress_store: ProgressStore,
) -> dict:
    return choose_variant(
        block,
        schema,
        metadata,
        response_metadata,
        answer_store,
        list_store,
        variants_key="content_variants",
        single_key="content",
        current_location=current_location,
        progress_store=progress_store,
    )


def transform_variants(
    block: ImmutableDict,
    schema: QuestionnaireSchema,
    metadata: MetadataProxy | None,
    response_metadata: MutableMapping,
    answer_store: AnswerStore,
    list_store: ListStore,
    current_location: LocationType,
    progress_store: ProgressStore,
) -> ImmutableDict:
    output_block = dict(block)
    if "question_variants" in block:
        question = choose_question_to_display(
            block,
            schema,
            metadata,
            response_metadata,
            answer_store,
            list_store,
            current_location,
            progress_store=progress_store,
        )
        output_block.pop("question_variants", None)
        output_block.pop("question", None)

        output_block["question"] = question

    if "content_variants" in block:
        content = choose_content_to_display(
            block,
            schema,
            metadata,
            response_metadata,
            answer_store,
            list_store,
            current_location,
            progress_store=progress_store,
        )
        output_block.pop("content_variants", None)
        output_block.pop("content", None)

        output_block["content"] = content

    if block["type"] in ("ListCollector", "PrimaryPersonListCollector"):
        list_operations = ["add_block", "edit_block", "remove_block"]
        for list_operation in list_operations:
            if block.get(list_operation):
                output_block[list_operation] = transform_variants(
                    block[list_operation],
                    schema,
                    metadata,
                    response_metadata,
                    answer_store,
                    list_store,
                    current_location,
                    progress_store=progress_store,
                )

    return ImmutableDict(output_block)
