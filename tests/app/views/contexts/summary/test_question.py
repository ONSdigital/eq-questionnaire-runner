# pylint: disable=too-many-lines
import pytest

from app.data_models import Answer, ListStore, ProgressStore, SupplementaryDataStore
from app.data_models.answer_store import AnswerStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.return_location import ReturnLocation
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.utilities.schema import load_schema_from_name
from app.views.contexts.summary.question import Question


def get_rule_evaluator(answer_store, list_store, schema, response_metadata=None):
    return RuleEvaluator(
        schema=schema,
        answer_store=answer_store,
        list_store=list_store,
        metadata={},
        response_metadata=response_metadata or {},
        location=None,
        progress_store=ProgressStore(),
        supplementary_data_store=SupplementaryDataStore(),
    )


def get_value_source_resolver(answer_store, list_store, schema, response_metadata=None):
    return ValueSourceResolver(
        answer_store=answer_store,
        list_store=list_store,
        metadata={},
        response_metadata=response_metadata or {},
        schema=schema,
        location=None,
        list_item_id=None,
        routing_path_block_ids=None,
        use_default_answer=True,
        progress_store=ProgressStore(),
        supplementary_data_store=SupplementaryDataStore(),
    )


def get_question_schema(answer_schema):
    return {
        "id": "question_id",
        "title": "Question title",
        "type": "General",
        "answers": [answer_schema],
    }


def address_questionnaire_schema(concatenation_type):
    return QuestionnaireSchema(
        {
            "sections": [
                {
                    "id": "address-section",
                    "groups": [
                        {
                            "blocks": [
                                {
                                    "type": "Question",
                                    "id": "what-is-your-address",
                                    "question": {
                                        "id": "what-is-your-address-question",
                                        "title": "What is your address?",
                                        "type": "General",
                                        "answers": [
                                            {
                                                "id": "building",
                                                "label": "Building",
                                                "mandatory": False,
                                                "type": "TextField",
                                                "default": "Government Buildings",
                                            },
                                            {
                                                "id": "address-line-1",
                                                "label": "Address Line 1",
                                                "mandatory": True,
                                                "type": "TextField",
                                            },
                                            {
                                                "id": "address-line-2",
                                                "label": "Address Line 2",
                                                "mandatory": False,
                                                "type": "TextField",
                                            },
                                            {
                                                "id": "address-line-3",
                                                "label": "Address Line 3",
                                                "mandatory": False,
                                                "type": "TextField",
                                            },
                                            {
                                                "id": "town-city",
                                                "label": "Town/City",
                                                "mandatory": False,
                                                "type": "TextField",
                                            },
                                            {
                                                "id": "county",
                                                "label": "County",
                                                "mandatory": False,
                                                "type": "TextField",
                                            },
                                            {
                                                "id": "postcode",
                                                "label": "Postcode",
                                                "mandatory": False,
                                                "type": "TextField",
                                            },
                                            {
                                                "id": "country",
                                                "label": "Country",
                                                "mandatory": False,
                                                "type": "TextField",
                                            },
                                        ],
                                        "summary": {
                                            "concatenation_type": concatenation_type
                                        },
                                    },
                                },
                            ],
                            "id": "address-group",
                        }
                    ],
                }
            ]
        }
    )


def address_question(
    answer_store,
    list_store,
    progress_store,
    schema,
    supplementary_data_store,
):
    question_schema = schema.get_questions("what-is-your-address-question")[0]
    return Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, schema),
        location=None,
        block_id="address-block",
        return_location=ReturnLocation(),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, schema
        ),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "question_title, answers, expected_title, expected_len",
    (
        (
            "Question title",
            [{"type": "Number", "id": "age-answer", "mandatory": True, "label": "Age"}],
            "Question title",
            1,
        ),
        ("Question title", [], "Question title", 0),
        (
            "",
            [{"type": "Number", "id": "age-answer", "mandatory": True, "label": "Age"}],
            "Age",
            1,
        ),
    ),
)
def test_create_question(
    question_title,
    answers,
    expected_title,
    expected_len,
    answer_store,
    list_store,
    progress_store,
    mock_schema,
    supplementary_data_store,
):
    # Given
    question_schema = {
        "id": "question_id",
        "title": question_title,
        "type": "GENERAL",
        "answers": answers,
    }

    # When
    question = Question(
        question_schema=question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, mock_schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert question.id == "question_id"
    assert question.title == expected_title
    assert len(question.answers) == expected_len


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "concatenation_type, concatenation_character",
    (
        ("Newline", "<br>"),
        ("Space", " "),
    ),
)
def test_concatenate_textfield_answers(
    concatenation_type,
    concatenation_character,
    list_store,
    progress_store,
    answer_store,
    supplementary_data_store,
):
    # Given
    schema = address_questionnaire_schema(concatenation_type)
    for answer in (
        Answer(answer_id="building", value="Main Building"),
        Answer(answer_id="address-line-1", value="Cardiff Rd"),
        Answer(answer_id="town-city", value="Newport"),
        Answer(answer_id="postcode", value="NP10 8XG"),
    ):
        answer_store.add_or_update(answer)

    question = address_question(
        answer_store,
        list_store,
        progress_store,
        schema,
        supplementary_data_store,
    )
    # Then
    assert (
        question.answers[0]["value"]
        == f"Main Building{concatenation_character}Cardiff Rd{concatenation_character}Newport{concatenation_character}NP10 8XG"
    )
    assert len(question.answers) == 1


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "concatenation_type, concatenation_character",
    (
        ("Newline", "<br>"),
        ("Space", " "),
    ),
)
def test_concatenate_textfield_answers_default(
    concatenation_type,
    concatenation_character,
    list_store,
    answer_store,
    progress_store,
    supplementary_data_store,
):
    # Given
    schema = address_questionnaire_schema(concatenation_type)
    for answer in (
        Answer(answer_id="address-line-1", value="Cardiff Rd"),
        Answer(answer_id="town-city", value="Newport"),
        Answer(answer_id="postcode", value="NP10 8XG"),
    ):
        answer_store.add_or_update(answer)

    # When
    question = address_question(
        answer_store,
        list_store,
        progress_store,
        schema,
        supplementary_data_store,
    )

    # Then
    assert (
        question.answers[0]["value"]
        == f"Government Buildings{concatenation_character}Cardiff Rd{concatenation_character}Newport{concatenation_character}NP10 8XG"
    )
    assert len(question.answers) == 1


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "concatenation_type, concatenation_character",
    (
        ("Newline", "<br>"),
        ("Space", " "),
    ),
)
def test_concatenate_number_and_checkbox_answers(
    concatenation_type,
    concatenation_character,
    list_store,
    answer_store,
    progress_store,
    mock_schema,
    supplementary_data_store,
):
    # Given
    answer_store.add_or_update(Answer(answer_id="age", value=7))
    answer_store.add_or_update(
        Answer(answer_id="estimate", value=["This age is an estimate"])
    )

    age_answer_schema = {
        "id": "age",
        "label": "Enter your age",
        "mandatory": False,
        "type": "Number",
    }
    checkbox_answer_schema = {
        "id": "estimate",
        "mandatory": False,
        "options": [
            {
                "label": "This age is an estimate",
                "value": "This age is an estimate",
            }
        ],
        "type": "Checkbox",
    }

    question_schema = {
        "id": "question_id",
        "title": "Question title",
        "type": "General",
        "answers": [age_answer_schema, checkbox_answer_schema],
        "summary": {"concatenation_type": concatenation_type},
    }

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, mock_schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert (
        question.answers[0]["value"]
        == f"7{concatenation_character}This age is an estimate"
    )
    assert len(question.answers) == 1


@pytest.mark.usefixtures("app")
def test_merge_date_range_answers(
    answer_store,
    list_store,
    progress_store,
    mock_schema,
    supplementary_data_store,
):
    # Given
    answer_store.add_or_update(Answer(answer_id="answer_1", value="13/02/2016"))
    answer_store.add_or_update(Answer(answer_id="answer_2", value="13/09/2016"))

    question_schema = {
        "id": "question_id",
        "title": "Question title",
        "type": "DateRange",
        "answers": [
            {"id": "answer_1", "label": "From", "type": "date"},
            {"id": "answer_2", "label": "To", "type": "date"},
        ],
    }

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, mock_schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert len(question.answers) == 1
    assert question.answers[0]["value"]["from"] == "13/02/2016"
    assert question.answers[0]["value"]["to"] == "13/09/2016"


@pytest.mark.usefixtures("app")
def test_merge_multiple_date_range_answers(
    answer_store,
    list_store,
    progress_store,
    mock_schema,
    supplementary_data_store,
):
    # Given
    for answer in (
        Answer(answer_id="answer_1", value="13/02/2016"),
        Answer(answer_id="answer_2", value="13/09/2016"),
        Answer(answer_id="answer_3", value="13/03/2016"),
        Answer(answer_id="answer_4", value="13/10/2016"),
    ):
        answer_store.add_or_update(answer)

    question_schema = {
        "id": "question_id",
        "title": "Question title",
        "type": "DateRange",
        "answers": [
            {"id": "answer_1", "label": "From", "type": "date"},
            {"id": "answer_2", "label": "To", "type": "date"},
            {"id": "answer_3", "label": "First period", "type": "date"},
            {"id": "answer_4", "label": "Second period", "type": "date"},
        ],
    }

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, mock_schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert len(question.answers) == 2
    assert question.answers[0]["value"]["from"] == "13/02/2016"
    assert question.answers[0]["value"]["to"] == "13/09/2016"
    assert question.answers[1]["value"]["from"] == "13/03/2016"
    assert question.answers[1]["value"]["to"] == "13/10/2016"


@pytest.mark.usefixtures("app")
def test_create_question_with_multiple_answers(
    answer_store,
    list_store,
    progress_store,
    mock_schema,
    supplementary_data_store,
):
    # Given
    for answer in (
        Answer(answer_id="answer_1", value="Han"),
        Answer(answer_id="answer_2", value="Solo"),
    ):
        answer_store.add_or_update(answer)

    question_schema = {
        "id": "question_id",
        "title": "Question title",
        "type": "GENERAL",
        "answers": [
            {"id": "answer_1", "label": "First name", "type": "text"},
            {"id": "answer_2", "label": "Surname", "type": "text"},
        ],
    }

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, mock_schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert len(question.answers) == 2
    assert question.answers[0]["value"] == "Han"
    assert question.answers[1]["value"] == "Solo"


@pytest.mark.usefixtures("app")
def test_checkbox_button_options(
    answer_store,
    list_store,
    progress_store,
    mock_schema,
    supplementary_data_store,
):
    # Given
    answer_store.add_or_update(
        Answer(answer_id="answer_1", value=["Light Side", "Dark Side"])
    )

    question_schema = {
        "id": "question_id",
        "title": "Question title",
        "type": "GENERAL",
        "answers": [
            {
                "id": "answer_1",
                "label": "Which side?",
                "type": "Checkbox",
                "options": [
                    {"label": "Light Side label", "value": "Light Side"},
                    {"label": "Dark Side label", "value": "Dark Side"},
                ],
            }
        ],
    }

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, mock_schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert len(question.answers[0]["value"]) == 2
    assert question.answers[0]["value"][0]["label"] == "Light Side label"
    assert question.answers[0]["value"][1]["label"] == "Dark Side label"


@pytest.mark.usefixtures("app")
def test_checkbox_button_detail_answer_empty(
    answer_store,
    list_store,
    progress_store,
    mock_schema,
    supplementary_data_store,
):
    # Given
    answer_store.add_or_update(Answer(answer_id="answer_1", value=["other", ""]))

    question_schema = {
        "id": "question_id",
        "title": "Question title",
        "type": "GENERAL",
        "answers": [
            {
                "id": "answer_1",
                "label": "Which side?",
                "type": "Checkbox",
                "options": [
                    {"label": "Light Side", "value": "Light Side"},
                    {
                        "label": "Other option label",
                        "value": "other",
                        "other": {"label": "Please specify other"},
                    },
                ],
            }
        ],
    }

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, mock_schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert len(question.answers[0]["value"]) == 1
    assert question.answers[0]["value"][0]["label"] == "Other option label"
    assert question.answers[0]["value"][0]["detail_answer_value"] is None


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "options, answers, expected_len, expected_value",
    (
        (
            [
                {"label": "Light Side", "value": "Light Side"},
                {
                    "label": "Other",
                    "value": "Other",
                    "detail_answer": {"id": "child_answer", "type": "TextField"},
                },
            ],
            [
                Answer(answer_id="answer_1", value=["Light Side", "Other"]),
                Answer(answer_id="child_answer", value="Test"),
            ],
            2,
            "Test",
        ),
        (
            [
                {"label": "1", "value": "1"},
                {
                    "label": "Other",
                    "value": "Other",
                    "detail_answer": {"id": "child_answer", "type": "Number"},
                },
            ],
            [
                Answer(answer_id="answer_1", value=["1", "Other"]),
                Answer(answer_id="child_answer", value=2),
            ],
            2,
            2,
        ),
    ),
)
def test_checkbox_answer_with_detail_answer_returns_the_value(
    options,
    answers,
    expected_len,
    expected_value,
    answer_store,
    list_store,
    progress_store,
    mock_schema,
    supplementary_data_store,
):
    # Given
    for answer in answers:
        answer_store.add_or_update(answer)

    question_schema = {
        "id": "question_id",
        "title": "Question title",
        "type": "GENERAL",
        "answers": [
            {
                "id": "answer_1",
                "label": "Which side?",
                "type": "Checkbox",
                "options": options,
            }
        ],
    }

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, mock_schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert len(question.answers[0]["value"]) == expected_len
    assert question.answers[0]["value"][1]["detail_answer_value"] == expected_value


@pytest.mark.usefixtures("app")
def test_checkbox_button_other_option_text(
    answer_store,
    list_store,
    progress_store,
    mock_schema,
    supplementary_data_store,
):
    # Given
    answer_store.add_or_update(
        Answer(answer_id="answer_1", value=["Light Side", "other"])
    )
    answer_store.add_or_update(Answer(answer_id="child_answer", value="Neither"))

    question_schema = {
        "id": "question_id",
        "title": "Question title",
        "type": "GENERAL",
        "answers": [
            {
                "id": "answer_1",
                "label": "Which side?",
                "type": "Checkbox",
                "options": [
                    {"label": "Light Side", "value": "Light Side"},
                    {
                        "label": "other",
                        "value": "other",
                        "detail_answer": {"id": "child_answer"},
                    },
                ],
            }
        ],
    }

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, mock_schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert len(question.answers[0]["value"]) == 2
    assert question.answers[0]["value"][0]["label"] == "Light Side"
    assert question.answers[0]["value"][1]["detail_answer_value"] == "Neither"


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "answer_type, options, answers, expected",
    (
        (
            "Radio",
            [
                {"label": 1, "value": 1},
                {
                    "label": "Other",
                    "value": "Other",
                    "detail_answer": {"id": "child_answer", "type": "Number"},
                },
            ],
            [
                Answer(answer_id="answer_1", value="Other"),
                Answer(answer_id="child_answer", value=1),
            ],
            1,
        ),
        (
            "Radio",
            [
                {
                    "label": "Other",
                    "value": "Other",
                    "detail_answer": {"id": "child_answer", "type": "TextField"},
                }
            ],
            [
                Answer(answer_id="answer_1", value="Other"),
                Answer(answer_id="child_answer", value="Test"),
            ],
            "Test",
        ),
    ),
)
def test_radio_answer_with_detail_answers_returns_correct_value(
    answer_type,
    options,
    answers,
    expected,
    answer_store,
    list_store,
    progress_store,
    mock_schema,
    supplementary_data_store,
):
    # Given
    for answer in answers:
        answer_store.add_or_update(answer)

    question_schema = {
        "id": "question_id",
        "title": "Question title",
        "type": "GENERAL",
        "answers": [
            {
                "id": "answer_1",
                "label": "How many cakes have you had today?",
                "type": answer_type,
                "options": options,
            }
        ],
    }

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, mock_schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert question.answers[0]["value"]["detail_answer_value"] == expected


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "answer_type, options, answers, expected",
    (
        (
            "Dropdown",
            [
                {"label": "Light Side label", "value": "Light Side"},
                {"label": "Dark Side label", "value": "Dark Side"},
            ],
            [Answer(answer_id="answer_1", value="Dark Side")],
            "Dark Side label",
        ),
        (
            "Dropdown",
            [{"label": "Light Side", "value": "Light Side"}],
            [],
            None,
        ),
        (
            "Radio",
            [{"label": "Light Side", "value": "Light Side"}],
            [],
            None,
        ),
        (
            "Checkbox",
            [{"label": "Light Side", "value": "Light Side"}],
            [Answer(answer_id="answer_1", value=[])],
            None,
        ),
    ),
)
def test_answer_types_selected_option_label(
    answer_type,
    options,
    answers,
    expected,
    answer_store,
    list_store,
    progress_store,
    mock_schema,
    supplementary_data_store,
):
    for answer in answers:
        answer_store.add_or_update(answer)

    question_schema = {
        "id": "question_id",
        "title": "Question title",
        "type": "GENERAL",
        "answers": [
            {
                "id": "answer_1",
                "label": "Which side?",
                "type": answer_type,
                "options": options,
            }
        ],
    }

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, mock_schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert question.answers[0]["value"] == expected


@pytest.mark.usefixtures("app")
def test_dynamic_checkbox_answer_options(
    answer_store,
    list_store,
    progress_store,
    mock_schema,
    dynamic_answer_options_schema,
    supplementary_data_store,
):
    # Given
    answer_schema = {
        "id": "dynamic-checkbox-answer",
        "label": "Which side?",
        "type": "Checkbox",
        **dynamic_answer_options_schema,
    }
    question_schema = get_question_schema(answer_schema)

    answer_store = AnswerStore(
        [
            {
                "answer_id": "dynamic-checkbox-answer",
                "value": ["2020-12-29", "2020-12-30", "2020-12-31"],
            }
        ]
    )

    response_metadata = {"started_at": "2021-01-01T09:00:00.220038+00:00"}

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(
            answer_store, list_store, mock_schema, response_metadata
        ),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema, response_metadata
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert question.answers[0]["value"] == [
        {
            "label": "Tuesday 29 December 2020",
            "detail_answer_value": None,
        },
        {"detail_answer_value": None, "label": "Wednesday 30 December 2020"},
    ]


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "answer_type, answer_store_value, expected",
    (
        (
            "Radio",
            "2020-12-29",
            {"detail_answer_value": None, "label": "Tuesday 29 December 2020"},
        ),
        (
            "Checkbox",
            ["2020-12-29", "2020-12-30"],
            [
                {
                    "label": "Tuesday 29 December 2020",
                    "detail_answer_value": None,
                },
                {
                    "detail_answer_value": None,
                    "label": "Wednesday 30 December 2020",
                },
            ],
        ),
        ("Dropdown", "2020-12-30", "Wednesday 30 December 2020"),
    ),
)
def test_dynamic_answer_options(
    answer_type,
    list_store,
    progress_store,
    answer_store_value,
    supplementary_data_store,
    expected,
    dynamic_answer_options_schema,
    mock_schema,
):
    # Given
    answer_id = f"dynamic-{answer_type.lower()}-answer"
    answer_schema = {
        "id": answer_id,
        "label": "Some label",
        "type": answer_type,
        **dynamic_answer_options_schema,
    }
    question_schema = get_question_schema(answer_schema)

    answer_store = AnswerStore([{"answer_id": answer_id, "value": answer_store_value}])
    response_metadata = {"started_at": "2021-01-01T09:00:00.220038+00:00"}
    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=mock_schema,
        rule_evaluator=get_rule_evaluator(
            answer_store, list_store, mock_schema, response_metadata
        ),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, mock_schema, response_metadata
        ),
        location=None,
        block_id="house-type",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert question.answers[0]["value"] == expected


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "answer_schema, answer_store, expected",
    (
        (
            {
                "id": "building",
                "label": "Building",
                "type": "TextField",
            },
            AnswerStore([{"answer_id": "building", "value": "Government Buildings"}]),
            "Government Buildings",
        ),
        (
            {
                "id": "building",
                "label": "Building",
                "type": "TextField",
            },
            AnswerStore(
                [{"answer_id": "building", "value": "<p>Government Buildings</p>"}]
            ),
            "&lt;p&gt;Government Buildings&lt;/p&gt;",
        ),
        (
            {
                "id": "building",
                "label": "Building",
                "type": "TextField",
                "default": "Government Buildings",
            },
            AnswerStore([]),
            "Government Buildings",
        ),
    ),
)
def test_get_answer(
    answer_schema,
    answer_store,
    expected,
    list_store,
    progress_store,
    supplementary_data_store,
):
    schema = address_questionnaire_schema("Newline")

    # Given
    question_schema = get_question_schema(answer_schema)

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, schema
        ),
        location=None,
        block_id="address-group",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert question.get_answer(answer_store, "building") == expected


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "answer_store, list_store, expected",
    (
        (
            AnswerStore(
                [
                    {"answer_id": "any-supermarket-answer", "value": "Yes"},
                    {
                        "answer_id": "supermarket-name",
                        "value": "Tesco",
                        "list_item_id": "awTNTI",
                    },
                    {
                        "answer_id": "supermarket-name",
                        "value": "Aldi",
                        "list_item_id": "FMOByU",
                    },
                    {"answer_id": "list-collector-answer", "value": "No"},
                    {
                        "answer_id": "based-checkbox-answer",
                        "value": ["Non UK based supermarkets"],
                    },
                    {
                        "answer_id": "percentage-of-shopping",
                        "value": 12,
                        "list_item_id": "awTNTI",
                    },
                    {
                        "answer_id": "percentage-of-shopping",
                        "value": 21,
                        "list_item_id": "FMOByU",
                    },
                ],
            ),
            ListStore([{"items": ["awTNTI", "FMOByU"], "name": "supermarkets"}]),
            [
                {
                    "currency": None,
                    "id": "percentage-of-shopping-awTNTI",
                    "label": "Percentage of shopping at Tesco",
                    "link": "/questionnaire/group/?list_item_id=awTNTI#percentage-of-shopping-awTNTI",
                    "type": "percentage",
                    "unit": None,
                    "unit_length": None,
                    "value": 12,
                    "decimal_places": 0,
                },
                {
                    "currency": None,
                    "id": "percentage-of-shopping-FMOByU",
                    "label": "Percentage of shopping at Aldi",
                    "link": "/questionnaire/group/?list_item_id=FMOByU#percentage-of-shopping-FMOByU",
                    "type": "percentage",
                    "unit": None,
                    "unit_length": None,
                    "value": 21,
                    "decimal_places": 0,
                },
                {
                    "currency": None,
                    "id": "based-checkbox-answer",
                    "label": "Are supermarkets UK or non UK based?",
                    "link": "/questionnaire/group/#based-checkbox-answer",
                    "type": "checkbox",
                    "unit": None,
                    "unit_length": None,
                    "value": [
                        {
                            "detail_answer_value": None,
                            "label": "Non UK based supermarkets",
                        }
                    ],
                    "decimal_places": None,
                },
            ],
        ),
    ),
)
def test_dynamic_answers(
    answer_store,
    list_store,
    progress_store,
    expected,
    supplementary_data_store,
):
    schema = load_schema_from_name("test_dynamic_answers_list_source", "en")

    # Given
    question_schema = {
        "dynamic_answers": {
            "values": {"source": "list", "identifier": "supermarkets"},
            "answers": [
                {
                    "label": {
                        "text": "Percentage of shopping at {transformed_value}",
                        "placeholders": [
                            {
                                "placeholder": "transformed_value",
                                "value": {
                                    "source": "answers",
                                    "identifier": "supermarket-name",
                                },
                            }
                        ],
                    },
                    "id": "percentage-of-shopping",
                    "mandatory": False,
                    "type": "Percentage",
                    "maximum": {"value": 100},
                    "decimal_places": 0,
                }
            ],
        },
        "answers": [
            {
                "id": "based-checkbox-answer",
                "label": "Are supermarkets UK or non UK based?",
                "instruction": "Select any answers that apply",
                "mandatory": False,
                "options": [
                    {
                        "label": "UK based supermarkets",
                        "value": "UK based supermarkets",
                    },
                    {
                        "label": "Non UK based supermarkets",
                        "value": "Non UK based supermarkets",
                    },
                ],
                "type": "Checkbox",
            }
        ],
        "id": "dynamic-answer-question",
        "title": "What percent of your shopping do you do at each of the following supermarket?",
        "type": "General",
    }

    # When
    question = Question(
        question_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        schema=schema,
        rule_evaluator=get_rule_evaluator(answer_store, list_store, schema),
        value_source_resolver=get_value_source_resolver(
            answer_store, list_store, schema
        ),
        location=None,
        block_id="group",
        return_location=ReturnLocation(),
        language="en",
        metadata={},
        response_metadata={},
        supplementary_data_store=supplementary_data_store,
    )

    # Then
    assert question.answers == expected
