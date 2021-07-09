from collections import abc

import pytest
from werkzeug.datastructures import ImmutableDict

from app.questionnaire.questionnaire_schema import QuestionnaireSchema


def assert_all_dict_values_are_hashable(data):
    for value in data.values():
        if isinstance(value, ImmutableDict):
            return assert_all_dict_values_are_hashable(value)
        if isinstance(value, tuple):
            return tuple(assert_all_dict_values_are_hashable(v) for v in value)

        assert isinstance(value, abc.Hashable)


def test_schema_json_is_immutable_and_hashable(question_schema):
    schema = QuestionnaireSchema(question_schema)
    json = schema.json
    with pytest.raises(TypeError) as e:
        json["sections"] = []

    assert str(e.value) == "'ImmutableDict' objects are immutable"
    assert_all_dict_values_are_hashable(json)


def test_schema_attributes_returns_hashable_values(question_schema):
    schema = QuestionnaireSchema(question_schema)
    for section in schema.get_sections():
        assert_all_dict_values_are_hashable(section)


def test_error_messages_are_immutable():
    schema = QuestionnaireSchema({})
    assert isinstance(schema.error_messages, ImmutableDict)


def test_parent_id_map_is_immutable():
    schema = QuestionnaireSchema({})
    assert isinstance(schema.parent_id_map, ImmutableDict)


def test_get_sections(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    assert len(schema.get_sections()) == 1


def test_get_section(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    section = schema.get_section("section1")
    assert section["title"] == "Section 1"


def test_get_summary_for_section(section_with_custom_summary):
    schema = QuestionnaireSchema(section_with_custom_summary)
    section_summary = schema.get_summary_for_section("section")

    expected_keys = {
        "type",
        "for_list",
        "title",
        "add_link_text",
        "empty_list_text",
        "item_title",
    }

    assert len(section_summary["items"]) == 1
    assert set(section_summary["items"][0].keys()) == expected_keys


def test_get_summary_for_section_does_not_exist(section_with_custom_summary):
    del section_with_custom_summary["sections"][0]["summary"]
    schema = QuestionnaireSchema(section_with_custom_summary)
    assert not schema.get_summary_for_section("section")


def test_get_show_on_completion_for_section(section_with_custom_summary):
    schema = QuestionnaireSchema(section_with_custom_summary)
    assert schema.show_summary_on_completion_for_section(section_id="section") is True


def test_get_blocks(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    assert len(schema.get_blocks()) == 1


def test_get_block(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    block = schema.get_block("block1")

    assert block["id"] == "block1"


def test_get_groups(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    assert len(schema.get_groups()) == 1


def test_get_group(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    group = schema.get_group("group1")

    assert group["title"] == "Group 1"


def test_get_questions(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    questions = schema.get_questions("question1")

    assert questions[0]["title"] == "Question 1"


def test_get_questions_with_variants(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    questions = schema.get_questions("question1")

    assert len(questions) == 2
    assert questions[0]["title"] == "Question 1, Yes"
    assert questions[1]["title"] == "Question 1, No"


def test_get_answers_by_answer_id_with_variants(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    answers = schema.get_answers_by_answer_id("answer1")
    assert len(answers) == 2
    assert answers[0]["label"] == "Answer 1 Variant 1"
    assert answers[1]["label"] == "Answer 1 Variant 2"


def test_get_answers_by_answer_id(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    answers = schema.get_answers_by_answer_id("answer1")
    assert len(answers) == 1
    assert answers[0]["label"] == "Answer 1"


def test_get_group_for_list_collector_child_block():
    survey_json = {
        "sections": [
            {
                "id": "section1",
                "groups": [
                    {
                        "id": "group",
                        "blocks": [
                            {
                                "id": "list-collector",
                                "type": "ListCollector",
                                "for_list": "list",
                                "question": {},
                                "add_block": {
                                    "id": "add-block",
                                    "type": "ListAddQuestion",
                                    "question": {},
                                },
                                "edit_block": {
                                    "id": "edit-block",
                                    "type": "ListEditQuestion",
                                    "question": {},
                                },
                                "remove_block": {
                                    "id": "remove-block",
                                    "type": "ListRemoveQuestion",
                                    "question": {},
                                },
                            }
                        ],
                    }
                ],
            }
        ]
    }

    schema = QuestionnaireSchema(survey_json)

    group = schema.get_group_for_block_id("add-block")

    assert group is not None
    assert group["id"] == "group"


def test_get_all_questions_for_block_question():
    block = {
        "id": "block1",
        "type": "Question",
        "title": "Block 1",
        "question": {
            "id": "question1",
            "title": "Question 1",
            "answers": [{"id": "answer1", "label": "Answer 1"}],
        },
    }

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert len(all_questions) == 1

    assert all_questions[0]["answers"][0]["id"] == "answer1"


def test_get_section_ids_by_list_name(sections_dependent_on_list_schema):
    schema = QuestionnaireSchema(sections_dependent_on_list_schema)
    when_blocks = schema.get_section_ids_dependent_on_list("list")

    assert len(when_blocks) == 1
    assert "section2" in when_blocks


def test_get_all_questions_for_block_question_variants():
    block = {
        "id": "block1",
        "type": "Question",
        "title": "Block 1",
        "question_variants": [
            {
                "question": {
                    "id": "question1",
                    "title": "Question 1",
                    "answers": [{"id": "answer1", "label": "Variant 1"}],
                },
                "when": [],
            },
            {
                "question": {
                    "id": "question1",
                    "title": "Question 1",
                    "answers": [{"id": "answer1", "label": "Variant 2"}],
                },
                "when": [],
            },
        ],
    }

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert len(all_questions) == 2

    assert all_questions[0]["answers"][0]["label"] == "Variant 1"
    assert all_questions[1]["answers"][0]["label"] == "Variant 2"


def test_get_all_questions_for_block_empty():
    block = {}

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert not all_questions


def test_get_answer_ids_for_block_no_variants(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    answer_ids = schema.get_answer_ids_for_block("block1")
    assert len(answer_ids) == 1
    assert answer_ids[0] == "answer1"


def test_get_answer_ids_for_block_with_variants(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    answer_ids = schema.get_answer_ids_for_block("block1")
    assert len(answer_ids) == 1
    assert answer_ids[0] == "answer1"


def test_get_default_answer_no_answer_in_answer_store(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    assert schema.get_default_answer("test") is None


def test_get_default_answer_no_default_in_schema(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    assert schema.get_default_answer("answer1") is None


def test_get_default_answer_single_question(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    answer = schema.get_default_answer("answer1")

    assert answer.answer_id == "answer1"
    assert answer.value == "test"


def test_get_relationship_collectors(mock_relationship_collector_schema):
    schema = QuestionnaireSchema(mock_relationship_collector_schema)
    collectors = schema.get_relationship_collectors()

    assert len(collectors) == 2
    assert collectors[0]["id"] == "relationships"
    assert collectors[1]["id"] == "not-people-relationship-collector"


def test_get_relationship_collectors_by_list_name(mock_relationship_collector_schema):
    schema = QuestionnaireSchema(mock_relationship_collector_schema)
    collectors = schema.get_relationship_collectors_by_list_name("people")

    assert len(collectors) == 1
    assert collectors[0]["id"] == "relationships"


def test_get_relationship_collectors_by_list_name_no_collectors(
    mock_relationship_collector_schema,
):
    schema = QuestionnaireSchema(mock_relationship_collector_schema)
    collectors = schema.get_relationship_collectors_by_list_name("not-a-list")

    assert not collectors


def test_answer_should_not_have_list_item_id_without_repeat_or_list_collector(
    question_schema,
):
    schema = QuestionnaireSchema(question_schema)

    assert schema.answer_should_have_list_item_id(answer_id="answer1") is False


def test_answer_should_have_list_item_id_within_repeat(section_with_repeating_list):
    schema = QuestionnaireSchema(section_with_repeating_list)

    assert schema.answer_should_have_list_item_id(answer_id="proxy-answer") is True


def test_answer_should_have_list_item_id_within_list_collector(
    list_collector_variant_schema,
):
    schema = QuestionnaireSchema(list_collector_variant_schema)

    assert schema.answer_should_have_list_item_id(answer_id="answer1") is True


def test_get_list_collector_for_list(list_collector_variant_schema):
    schema = QuestionnaireSchema(list_collector_variant_schema)
    section = schema.get_section("section")

    result = QuestionnaireSchema.get_list_collector_for_list(section, for_list="people")

    assert result["id"] == "block1"

    filtered_result = QuestionnaireSchema.get_list_collector_for_list(
        section, for_list="people"
    )

    assert filtered_result == result

    no_result = QuestionnaireSchema.get_list_collector_for_list(
        section, for_list="not-valid"
    )

    assert no_result is None


def test_has_address_lookup_answer():
    question = {
        "type": "General",
        "id": "address-question",
        "title": "What is your current address?",
        "answers": [
            {
                "id": "address-answer",
                "mandatory": True,
                "type": "Address",
                "lookup_options": {
                    "address_type": "Residential",
                    "region_code": "GB-ENG",
                },
            }
        ],
    }

    has_lookup_answer = QuestionnaireSchema.has_address_lookup_answer(question)
    assert has_lookup_answer


def test_doesnt_have_address_lookup_answer():
    question = {
        "type": "General",
        "id": "address-question",
        "title": "What is your current address?",
        "answers": [
            {
                "id": "address-answer",
                "mandatory": True,
                "type": "Address",
            }
        ],
    }

    has_lookup_answer = QuestionnaireSchema.has_address_lookup_answer(question)
    assert not has_lookup_answer
