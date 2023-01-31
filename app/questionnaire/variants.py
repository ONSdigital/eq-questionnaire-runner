from werkzeug.datastructures import ImmutableDict

from app.questionnaire.rules.rule_evaluator import RuleEvaluator


def choose_variant(
    block,
    schema,
    metadata,
    response_metadata,
    answer_store,
    list_store,
    variants_key,
    single_key,
    current_location,
):
    if block.get(single_key):
        return block[single_key]
    for variant in block.get(variants_key, []):
        when_rules = variant["when"]

        when_rule_evaluator = RuleEvaluator(
            schema,
            answer_store,
            list_store,
            metadata,
            response_metadata,
            location=current_location,
        )

        if when_rule_evaluator.evaluate(when_rules):
            return variant[single_key]


def choose_question_to_display(
    block,
    schema,
    metadata,
    response_metadata,
    answer_store,
    list_store,
    current_location,
):
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
    )


def choose_content_to_display(
    block,
    schema,
    metadata,
    response_metadata,
    answer_store,
    list_store,
    current_location,
):
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
    )


def transform_variants(
    block,
    schema,
    metadata,
    response_metadata,
    answer_store,
    list_store,
    current_location,
):
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
                )

    return ImmutableDict(output_block)
