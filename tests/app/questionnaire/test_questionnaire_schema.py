from app.questionnaire.questionnaire_schema import QuestionnaireSchema


def test_get_sections(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    assert len(schema.get_sections()) == 1


def test_get_section(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    section = schema.get_section('section1')
    assert section['title'] == 'Section 1'


def test_get_blocks(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    assert len(schema.get_blocks()) == 1


def test_get_block(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    block = schema.get_block('block1')

    assert block['id'] == 'block1'


def test_get_groups(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    assert len(schema.get_groups()) == 1


def test_get_group(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    group = schema.get_group('group1')

    assert group['title'] == 'Group 1'


def test_get_questions_with_variants(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    questions = schema.get_questions('question1')

    assert len(questions) == 2
    assert questions[0]['title'] == 'Question 1, Yes'
    assert questions[1]['title'] == 'Question 1, No'


def test_get_questions(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    questions = schema.get_questions('question1')

    assert questions[0]['title'] == 'Question 1'


def test_schema_answers(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    answers = schema.get_answer_ids()
    assert len(answers) == 1


def test_get_answers_with_variants(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    answers = schema.get_answers_by_answer_id('answer1')
    assert len(answers) == 2
    assert answers[0]['label'] == 'Answer 1 Variant 1'
    assert answers[1]['label'] == 'Answer 1 Variant 2'


def test_get_answers(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    answers = schema.get_answers_by_answer_id('answer1')
    assert len(answers) == 1
    assert answers[0]['label'] == 'Answer 1'


def test_get_summary_and_confirmation_blocks_returns_only_summary():
    survey_json = {
        'sections': [
            {
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group1',
                        'blocks': [
                            {'id': 'questionnaire-block', 'type': 'Question'},
                            {'id': 'summary-block', 'type': 'Summary'},
                            {'id': 'confirmation-block', 'type': 'Confirmation'},
                        ],
                    }
                ],
            }
        ]
    }

    schema = QuestionnaireSchema(survey_json)

    summary_and_confirmation_blocks = schema.get_summary_and_confirmation_blocks()

    assert len(summary_and_confirmation_blocks) == 2
    assert 'summary-block' in summary_and_confirmation_blocks
    assert 'confirmation-block' in summary_and_confirmation_blocks


def test_group_has_questions_returns_true_when_group_has_questionnaire_blocks():
    survey_json = {
        'sections': [
            {
                'id': 'section1',
                'groups': [
                    {
                        'id': 'question-group',
                        'blocks': [
                            {'id': 'introduction', 'type': 'Introduction'},
                            {'id': 'question', 'type': 'Question'},
                        ],
                    }
                ],
            }
        ]
    }

    schema = QuestionnaireSchema(survey_json)

    assert schema.group_has_questions('question-group')


def test_group_has_questions_returns_false_when_group_doesnt_have_questionnaire_blocks():
    survey_json = {
        'sections': [
            {
                'id': 'section1',
                'groups': [
                    {
                        'id': 'non-question-group',
                        'blocks': [{'id': 'summary-block', 'type': 'Summary'}],
                    }
                ],
            }
        ]
    }

    schema = QuestionnaireSchema(survey_json)

    assert not schema.group_has_questions('non-question-group')


def test_is_summary():
    survey_json = {
        'sections': [
            {
                'id': 'section-1',
                'groups': [
                    {'id': 'group-1', 'blocks': [{'id': 'block-1', 'type': 'Summary'}]}
                ],
            }
        ]
    }

    schema = QuestionnaireSchema(survey_json)
    assert schema.is_summary_section(schema.get_section('section-1'))
    assert schema.is_summary_group(schema.get_group('group-1'))
    assert not schema.is_confirmation_section(schema.get_section('section-1'))
    assert not schema.is_confirmation_group(schema.get_group('group-1'))


def test_is_confirmation():
    survey_json = {
        'sections': [
            {
                'id': 'section-1',
                'groups': [
                    {
                        'id': 'group-1',
                        'blocks': [{'id': 'block-1', 'type': 'Confirmation'}],
                    }
                ],
            }
        ]
    }

    schema = QuestionnaireSchema(survey_json)
    assert schema.is_confirmation_section(schema.get_section('section-1'))
    assert schema.is_confirmation_group(schema.get_group('group-1'))
    assert not schema.is_summary_section(schema.get_section('section-1'))
    assert not schema.is_summary_group(schema.get_group('group-1'))


def test_get_group_for_list_collector_child_block():
    survey_json = {
        'sections': [
            {
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group',
                        'blocks': [
                            {
                                'id': 'list-collector',
                                'type': 'ListCollector',
                                'for_list': 'list',
                                'question': {},
                                'add_block': {
                                    'id': 'add-block',
                                    'type': 'ListAddQuestion',
                                    'question': {},
                                },
                                'edit_block': {
                                    'id': 'edit-block',
                                    'type': 'ListEditQuestion',
                                    'question': {},
                                },
                                'remove_block': {
                                    'id': 'remove-block',
                                    'type': 'ListRemoveQuestion',
                                    'question': {},
                                },
                            }
                        ],
                    }
                ],
            }
        ]
    }

    schema = QuestionnaireSchema(survey_json)

    group = schema.get_group_for_block_id('add-block')

    assert group is not None
    assert group['id'] == 'group'


def test_get_all_questions_for_block_question():
    block = {
        'id': 'block1',
        'type': 'Question',
        'title': 'Block 1',
        'question': {
            'id': 'question1',
            'title': 'Question 1',
            'answers': [{'id': 'answer1', 'label': 'Answer 1'}],
        },
    }

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert len(all_questions) == 1

    assert all_questions[0]['answers'][0]['id'] == 'answer1'


def test_get_all_questions_for_block_question_variants():
    block = {
        'id': 'block1',
        'type': 'Question',
        'title': 'Block 1',
        'question_variants': [
            {
                'question': {
                    'id': 'question1',
                    'title': 'Question 1',
                    'answers': [{'id': 'answer1', 'label': 'Variant 1'}],
                },
                'when': [],
            },
            {
                'question': {
                    'id': 'question1',
                    'title': 'Question 1',
                    'answers': [{'id': 'answer1', 'label': 'Variant 2'}],
                },
                'when': [],
            },
        ],
    }

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert len(all_questions) == 2

    assert all_questions[0]['answers'][0]['label'] == 'Variant 1'
    assert all_questions[1]['answers'][0]['label'] == 'Variant 2'


def test_get_all_questions_for_block_empty():
    block = {}

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert not all_questions


def test_get_default_answer_no_answer_in_answer_store(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    assert schema.get_default_answer('test') is None


def test_get_default_answer_no_default_in_schema(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    assert schema.get_default_answer('answer1') is None


def test_get_default_answer_single_question(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    answer = schema.get_default_answer('answer1')

    assert answer.answer_id == 'answer1'
    assert answer.value == 'test'


def test_get_relationship_collectors(relationship_collector_schema):
    schema = QuestionnaireSchema(relationship_collector_schema)
    answer = schema.get_relationship_collectors()

    assert len(answer) == 2
    assert answer[0]['id'] == 'relationships'
    assert answer[1]['id'] == 'relationships-that-dont-point-to-list-collector'


def test_get_relationship_collectors_by_list_name(relationship_collector_schema):
    schema = QuestionnaireSchema(relationship_collector_schema)
    answer = schema.get_relationship_collectors_by_list_name('people')

    assert len(answer) == 1
    assert answer[0]['id'] == 'relationships'


def test_get_relationship_collectors_by_list_name_no_collectors(
    relationship_collector_schema
):
    schema = QuestionnaireSchema(relationship_collector_schema)
    answer = schema.get_relationship_collectors_by_list_name('not-a-list')

    assert not answer


def test_get_list_item_id_for_answer_id_without_list_item_id(
    section_with_repeating_list
):
    schema = QuestionnaireSchema(section_with_repeating_list)

    expected_list_item_id = None

    list_item_id = schema.get_list_item_id_for_answer_id(
        answer_id='answer1', list_item_id=expected_list_item_id
    )

    assert list_item_id == expected_list_item_id


def test_get_list_item_id_for_answer_id_without_repeat_or_list_collector(
    question_schema
):
    schema = QuestionnaireSchema(question_schema)

    list_item_id = schema.get_list_item_id_for_answer_id(
        answer_id='answer1', list_item_id='abc123'
    )

    assert list_item_id is None


def test_get_answer_within_repeat_with_list_item_id(section_with_repeating_list):
    schema = QuestionnaireSchema(section_with_repeating_list)

    expected_list_item_id = 'abc123'

    list_item_id = schema.get_list_item_id_for_answer_id(
        answer_id='proxy-answer', list_item_id=expected_list_item_id
    )

    assert list_item_id == expected_list_item_id


def test_get_answer_within_list_collector_with_list_item_id(
    list_collector_variant_schema
):
    schema = QuestionnaireSchema(list_collector_variant_schema)

    expected_list_item_id = 'abc123'

    list_item_id = schema.get_list_item_id_for_answer_id(
        answer_id='answer1', list_item_id=expected_list_item_id
    )

    assert list_item_id == expected_list_item_id
