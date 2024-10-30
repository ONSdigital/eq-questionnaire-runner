from typing import Mapping

from werkzeug.datastructures import ImmutableDict

from app.data_models.data_stores import DataStores
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.utilities.types import LocationType


# Type ignore: validation should ensure the variant exists when this is called
def choose_variant(  # type: ignore
    block: Mapping,
    schema: QuestionnaireSchema,
    data_stores: DataStores,
    variants_key: str,
    single_key: str,
    current_location: LocationType,
) -> dict:
    if block.get(single_key):
        # Type ignore: the key passed in will be for a dictionary
        return block[single_key]  # type: ignore
    for variant in block.get(variants_key, []):
        when_rules = variant["when"]
        when_rule_evaluator = RuleEvaluator(
            schema,
            data_stores=data_stores,
            location=current_location,
            value_source_resolver=ValueSourceResolver(
                data_stores=data_stores,
                schema=schema,
                location=current_location,
                use_default_answer=True,
                list_item_id=current_location.list_item_id,
            ),
        )

        if when_rule_evaluator.evaluate(when_rules):
            # Type ignore: question/content key is for a dictionary
            return variant[single_key]  # type: ignore


def choose_question_to_display(
    block: ImmutableDict,
    schema: QuestionnaireSchema,
    data_stores: DataStores,
    current_location: LocationType,
) -> dict:
    return choose_variant(
        block,
        schema,
        data_stores,
        variants_key="question_variants",
        single_key="question",
        current_location=current_location,
    )


def choose_content_to_display(
    block: ImmutableDict,
    schema: QuestionnaireSchema,
    data_stores: DataStores,
    current_location: LocationType,
) -> dict:
    return choose_variant(
        block,
        schema,
        data_stores,
        variants_key="content_variants",
        single_key="content",
        current_location=current_location,
    )


def transform_variants(
    block: ImmutableDict,
    schema: QuestionnaireSchema,
    data_stores: DataStores,
    current_location: LocationType,
) -> ImmutableDict:
    output_block = dict(block)
    if "question_variants" in block:
        question = choose_question_to_display(
            block,
            schema,
            data_stores,
            current_location,
        )
        output_block.pop("question_variants", None)
        output_block.pop("question", None)

        output_block["question"] = question

    if "content_variants" in block:
        content = choose_content_to_display(
            block,
            schema,
            data_stores,
            current_location,
        )
        output_block.pop("content_variants", None)
        output_block.pop("content", None)

        output_block["content"] = content

    if block["type"] in {"ListCollector", "PrimaryPersonListCollector"}:
        list_operations = ["add_block", "edit_block", "remove_block"]
        for list_operation in list_operations:
            if block.get(list_operation):
                output_block[list_operation] = transform_variants(
                    block[list_operation],
                    schema,
                    data_stores,
                    current_location,
                )

    return ImmutableDict(output_block)
