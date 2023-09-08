from datetime import datetime, timezone

import pytest

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.routing_path import RoutingPath
from app.submitter.convert_payload_0_0_1 import convert_answers_to_payload_0_0_1
from app.submitter.converter_v2 import get_payload_data
from tests.app.submitter.conftest import get_questionnaire_store
from tests.app.submitter.schema import make_schema

SUBMITTED_AT = datetime.now(timezone.utc)


def create_answer(answer_id, value):
    return {"answer_id": answer_id, "value": value}


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_convert_answers_v2_to_payload_0_0_1_with_key_error(version):
    questionnaire_store = get_questionnaire_store(version)

    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("ABC", "2016-01-01").to_dict(),
            Answer("DEF", "2016-03-30").to_dict(),
            Answer("GHI", "2016-05-30").to_dict(),
        ]
    )

    question = {
        "id": "question-1",
        "type": "General",
        "answers": [
            {"id": "LMN", "type": "TextField", "q_code": "001"},
            {"id": "DEF", "type": "TextField", "q_code": "002"},
            {"id": "JKL", "type": "TextField", "q_code": "003"},
        ],
    }

    questionnaire = make_schema("0.0.1", "section-1", "group-1", "block-1", question)

    full_routing_path = [
        RoutingPath(block_ids=["block-1"], section_id="section-1", list_item_id=None)
    ]
    answer_object = convert_answers_to_payload_0_0_1(
        metadata=questionnaire_store.metadata,
        response_metadata=questionnaire_store.response_metadata,
        answer_store=questionnaire_store.answer_store,
        list_store=questionnaire_store.list_store,
        schema=QuestionnaireSchema(questionnaire),
        full_routing_path=full_routing_path,
        progress_store=questionnaire_store.progress_store,
        supplementary_data_store=questionnaire_store.supplementary_data_store,
    )
    assert answer_object["002"] == "2016-03-30"
    assert len(answer_object) == 1


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_answer_with_zero(version):
    questionnaire_store = get_questionnaire_store(version)

    questionnaire_store.answer_store = AnswerStore([Answer("GHI", 0).to_dict()])

    question = {
        "id": "question-2",
        "type": "General",
        "answers": [{"id": "GHI", "type": "TextField", "q_code": "003"}],
    }

    questionnaire = make_schema("0.0.1", "section-1", "group-1", "block-1", question)

    full_routing_path = [
        RoutingPath(block_ids=["block-1"], section_id="section-1", list_item_id=None)
    ]

    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    assert data_payload["003"] == "0"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_answer_with_float(version):
    questionnaire_store = get_questionnaire_store(version)

    questionnaire_store.answer_store = AnswerStore([Answer("GHI", 10.02).to_dict()])

    question = {
        "id": "question-2",
        "type": "General",
        "answers": [{"id": "GHI", "type": "TextField", "q_code": "003"}],
    }

    questionnaire = make_schema("0.0.1", "section-1", "group-1", "block-1", question)

    full_routing_path = [
        RoutingPath(block_ids=["block-1"], section_id="section-1", list_item_id=None)
    ]

    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Check the converter correctly
    assert data_payload["003"] == "10.02"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_answer_with_string(version):
    questionnaire_store = get_questionnaire_store(version)

    questionnaire_store.answer_store = AnswerStore(
        [Answer("GHI", "String test + !").to_dict()]
    )

    question = {
        "id": "question-2",
        "type": "General",
        "answers": [{"id": "GHI", "type": "TextField", "q_code": "003"}],
    }

    questionnaire = make_schema("0.0.1", "section-1", "group-1", "block-1", question)

    full_routing_path = [
        RoutingPath(block_ids=["block-1"], section_id="section-1", list_item_id=None)
    ]

    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Check the converter correctly
    assert data_payload["003"] == "String test + !"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_answer_without_qcode(version):
    questionnaire_store = get_questionnaire_store(version)

    questionnaire_store.answer_store = AnswerStore(
        [Answer("GHI", "String test + !").to_dict()]
    )

    question = {
        "id": "question-2",
        "type": "General",
        "answers": [{"id": "GHI", "type": "TextField"}],
    }

    questionnaire = make_schema("0.0.1", "section-1", "group-1", "block-1", question)

    full_routing_path = [
        RoutingPath(block_ids=["block-1"], section_id="section-1", list_item_id=None)
    ]

    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    assert not data_payload


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_converter_checkboxes_with_q_codes(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(block_ids=["crisps"], section_id="food")]
    questionnaire_store.answer_store = AnswerStore(
        [Answer("crisps-answer", ["Ready salted", "Sweet chilli"]).to_dict()]
    )

    question = {
        "id": "crisps-question",
        "type": "General",
        "answers": [
            {
                "id": "crisps-answer",
                "type": "Checkbox",
                "options": [
                    {"label": "Ready salted", "value": "Ready salted", "q_code": "1"},
                    {"label": "Sweet chilli", "value": "Sweet chilli", "q_code": "2"},
                    {
                        "label": "Cheese and onion",
                        "value": "Cheese and onion",
                        "q_code": "3",
                    },
                    {
                        "label": "Other",
                        "q_code": "4",
                        "description": "Choose any other flavour",
                        "value": "Other",
                        "detail_answer": {
                            "mandatory": True,
                            "id": "other-answer-mandatory",
                            "label": "Please specify other",
                            "type": "TextField",
                        },
                    },
                ],
            }
        ],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "favourite-food", "crisps", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 2
    assert data_payload["1"] == "Ready salted"
    assert data_payload["2"] == "Sweet chilli"


@pytest.mark.parametrize(
    "detail_answer_q_code_field, expected_data_length, version",
    [
        ({"q_code": "401"}, 3, None),
        ({}, 2, None),
        ({"q_code": "401"}, 3, AuthPayloadVersion.V2),
        ({}, 2, AuthPayloadVersion.V2),
    ],
)
def test_converter_checkboxes_with_q_codes_and_other_value(
    detail_answer_q_code_field, expected_data_length, version
):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(block_ids=["crisps"], section_id="food")]

    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("crisps-answer", ["Ready salted", "Other"]).to_dict(),
            Answer("other-answer-mandatory", "Bacon").to_dict(),
        ]
    )

    question = {
        "id": "crisps-question",
        "type": "General",
        "answers": [
            {
                "id": "crisps-answer",
                "type": "Checkbox",
                "options": [
                    {"label": "Ready salted", "value": "Ready salted", "q_code": "1"},
                    {"label": "Sweet chilli", "value": "Sweet chilli", "q_code": "2"},
                    {
                        "label": "Cheese and onion",
                        "value": "Cheese and onion",
                        "q_code": "3",
                    },
                    {
                        "label": "Other",
                        "q_code": "4",
                        "description": "Choose any other flavour",
                        "value": "Other",
                        "detail_answer": {
                            "mandatory": True,
                            "id": "other-answer-mandatory",
                            "label": "Please specify other",
                            "type": "TextField",
                            **detail_answer_q_code_field,
                        },
                    },
                ],
            }
        ],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "favourite-food", "crisps", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == expected_data_length
    assert data_payload["1"] == "Ready salted"
    assert data_payload["4"] == "Bacon"

    # If detail answer has a q_code then that should be used in the data outputted in the payload
    if detail_answer_q_code_field:
        assert data_payload[detail_answer_q_code_field["q_code"]] == "Bacon"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_converter_checkboxes_with_missing_detail_answer_value_in_answer_store(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(block_ids=["crisps"], section_id="food")]

    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("crisps-answer", ["Ready salted", "Other"]).to_dict(),
        ]
    )

    question = {
        "id": "crisps-question",
        "type": "General",
        "answers": [
            {
                "id": "crisps-answer",
                "type": "Checkbox",
                "options": [
                    {"label": "Ready salted", "value": "Ready salted", "q_code": "1"},
                    {"label": "Sweet chilli", "value": "Sweet chilli", "q_code": "2"},
                    {
                        "label": "Cheese and onion",
                        "value": "Cheese and onion",
                        "q_code": "3",
                    },
                    {
                        "label": "Other",
                        "q_code": "4",
                        "description": "Choose any other flavour",
                        "value": "Other",
                        "detail_answer": {
                            "mandatory": False,
                            "id": "other-answer-mandatory",
                            "label": "Please specify other",
                            "type": "TextField",
                        },
                    },
                ],
            }
        ],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "favourite-food", "crisps", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 2
    assert data_payload["1"] == "Ready salted"
    assert data_payload["4"] == "Other"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_converter_checkboxes_with_missing_q_codes_uses_answer_q_code(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(block_ids=["crisps"], section_id="food")]

    questionnaire_store.answer_store = AnswerStore(
        [Answer("crisps-answer", ["Ready salted", "Sweet chilli"]).to_dict()]
    )

    question = {
        "id": "crisps-question",
        "type": "General",
        "answers": [
            {
                "id": "crisps-answer",
                "type": "Checkbox",
                "q_code": "0",
                "options": [
                    {"label": "Ready salted", "value": "Ready salted", "q_code": "1"},
                    {"label": "Sweet chilli", "value": "Sweet chilli"},
                    {
                        "label": "Cheese and onion",
                        "value": "Cheese and onion",
                        "q_code": "3",
                    },
                    {
                        "label": "Other",
                        "q_code": "4",
                        "description": "Choose any other flavour",
                        "value": "Other",
                        "detail_answer": {
                            "mandatory": True,
                            "id": "other-answer-mandatory",
                            "label": "Please specify other",
                            "type": "TextField",
                        },
                    },
                ],
            }
        ],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "favourite-food", "crisps", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 1
    assert data_payload["0"], "['Ready salted' == 'Sweet chilli']"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_converter_q_codes_for_empty_strings(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(block_ids=["crisps"], section_id="food")]
    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("crisps-answer", "").to_dict(),
            Answer("other-crisps-answer", "Ready salted").to_dict(),
        ]
    )

    question = {
        "id": "crisps-question",
        "type": "General",
        "answers": [
            {"id": "crisps-answer", "type": "TextArea", "options": [], "q_code": "1"},
            {
                "id": "other-crisps-answer",
                "type": "TextArea",
                "options": [],
                "q_code": "2",
            },
        ],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "favourite-food", "crisps", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 1
    assert data_payload["2"] == "Ready salted"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_radio_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(
            block_ids=["radio-block"], section_id="section-1", list_item_id=None
        )
    ]
    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("radio-answer", "Coffee").to_dict(),
            Answer("other-answer-mandatory", "Water").to_dict(),
        ],
    )

    question = {
        "id": "radio-question",
        "type": "General",
        "answers": [
            {
                "type": "Radio",
                "id": "radio-answer",
                "q_code": "1",
                "options": [
                    {"label": "Coffee", "value": "Coffee"},
                    {"label": "Tea", "value": "Tea"},
                    {
                        "label": "Other",
                        "value": "Other",
                        "detail_answer": {
                            "mandatory": True,
                            "id": "other-answer-mandatory",
                            "label": "Please specify other",
                            "type": "TextField",
                            "q_code": "101",
                        },
                    },
                ],
            }
        ],
    }
    questionnaire = make_schema(
        "0.0.1", "section-1", "radio-block", "radio-block", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 2
    assert data_payload["1"] == "Coffee"
    assert data_payload["101"] == "Water"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_number_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(
            block_ids=["number-block"], section_id="section-1", list_item_id=None
        )
    ]
    questionnaire_store.answer_store = AnswerStore(
        [Answer("number-answer", 0.9999).to_dict()]
    )

    question = {
        "id": "number-question",
        "type": "General",
        "answers": [{"id": "number-answer", "type": "Number", "q_code": "1"}],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "number-block", "number-block", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 1
    assert data_payload["1"] == "0.9999"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_percentage_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(
            block_ids=["percentage-block"], section_id="section-1", list_item_id=None
        )
    ]
    questionnaire_store.answer_store = AnswerStore(
        [Answer("percentage-answer", 100).to_dict()]
    )

    question = {
        "id": "percentage-question",
        "type": "General",
        "answers": [{"id": "percentage-answer", "type": "Percentage", "q_code": "1"}],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "percentage-block", "percentage-block", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 1
    assert data_payload["1"] == "100"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_textarea_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(
            block_ids=["textarea-block"], section_id="section-1", list_item_id=None
        )
    ]
    questionnaire_store.answer_store = AnswerStore(
        [Answer("textarea-answer", "example text.").to_dict()]
    )

    question = {
        "id": "textarea-question",
        "type": "General",
        "answers": [{"id": "textarea-answer", "q_code": "1", "type": "TextArea"}],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "textarea-block", "textarea-block", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 1
    assert data_payload["1"] == "example text."


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_currency_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(
            block_ids=["currency-block"], section_id="section-1", list_item_id=None
        )
    ]
    questionnaire_store.answer_store = AnswerStore(
        [Answer("currency-answer", 99.99).to_dict()]
    )

    question = {
        "id": "currency-question",
        "type": "General",
        "answers": [{"id": "currency-answer", "type": "Currency", "q_code": "1"}],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "currency-block", "currency-block", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 1
    assert data_payload["1"] == "99.99"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_dropdown_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(
            block_ids=["dropdown-block"], section_id="section-1", list_item_id=None
        )
    ]
    questionnaire_store.answer_store = AnswerStore(
        [Answer("dropdown-answer", "Liverpool").to_dict()]
    )

    question = {
        "id": "dropdown-question",
        "type": "General",
        "answers": [
            {
                "id": "dropdown-answer",
                "type": "Dropdown",
                "q_code": "1",
                "options": [
                    {"label": "Liverpool", "value": "Liverpool"},
                    {"label": "Chelsea", "value": "Chelsea"},
                    {"label": "Rugby is better!", "value": "Rugby is better!"},
                ],
            }
        ],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "dropdown-block", "dropdown-block", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 1
    assert data_payload["1"] == "Liverpool"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_date_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(block_ids=["date-block"], section_id="section-1")]

    questionnaire_store.answer_store = AnswerStore(
        [
            create_answer("single-date-answer", "1990-02-01"),
            create_answer("month-year-answer", "1990-01"),
        ]
    )

    question = {
        "id": "single-date-question",
        "type": "General",
        "answers": [
            {"id": "single-date-answer", "type": "Date", "q_code": "1"},
            {"id": "month-year-answer", "type": "MonthYearDate", "q_code": "2"},
        ],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "date-block", "date-block", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 2
    assert data_payload["1"] == "01/02/1990"
    assert data_payload["2"] == "01/1990"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_unit_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(block_ids=["unit-block"], section_id="section-1")]
    questionnaire_store.answer_store = AnswerStore(
        [Answer("unit-answer", 10).to_dict()]
    )

    question = {
        "id": "unit-question",
        "type": "General",
        "answers": [{"id": "unit-answer", "type": "Unit", "q_code": "1"}],
    }

    questionnaire = make_schema(
        "0.0.1", "section-1", "unit-block", "unit-block", question
    )

    # When
    schema = QuestionnaireSchema(questionnaire)

    data_payload = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        full_routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Then
    assert len(data_payload) == 1
    assert data_payload["1"] == "10"
