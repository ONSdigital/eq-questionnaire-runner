# pylint: disable=too-many-lines
from datetime import datetime, timezone

import pytest

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.supplementary_data_store import SupplementaryDataStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.routing_path import RoutingPath
from app.submitter.converter_v2 import get_payload_data
from app.utilities.json import json_dumps, json_loads
from app.utilities.make_immutable import make_immutable
from app.utilities.schema import load_schema_from_name
from tests.app.submitter.conftest import get_questionnaire_store
from tests.app.submitter.schema import make_schema

SUBMITTED_AT = datetime.now(timezone.utc)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_convert_answers_v2_to_payload_0_0_3(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(["about you", "where you live"], section_id="household-section")
    ]

    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("name", "Joe Bloggs", None).to_dict(),
            Answer("address", "62 Somewhere", None).to_dict(),
        ]
    )

    questionnaire = {
        "survey_id": "021",
        "data_version": "0.0.3",
        "sections": [
            {
                "id": "household-section",
                "groups": [
                    {
                        "id": "personal details",
                        "blocks": [
                            {
                                "id": "about you",
                                "type": "Question",
                                "question": {
                                    "id": "crisps-question",
                                    "type": "General",
                                    "answers": [{"id": "name", "type": "TextField"}],
                                },
                            }
                        ],
                    },
                    {
                        "id": "household",
                        "blocks": [
                            {
                                "id": "where you live",
                                "type": "Question",
                                "question": {
                                    "id": "crisps-question",
                                    "type": "General",
                                    "answers": [{"id": "address", "type": "TextField"}],
                                },
                            }
                        ],
                    },
                ],
            }
        ],
    }

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
    assert len(data_payload["answers"]) == 2
    assert data_payload["answers"][0].value == "Joe Bloggs"
    assert data_payload["answers"][1].value, "62 Somewhere"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_convert_payload_0_0_3_multiple_answers(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(["crisps"], section_id="section-1")]
    answers = AnswerStore(
        [Answer("crisps-answer", ["Ready salted", "Sweet chilli"]).to_dict()]
    )
    questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "favourite-food",
        "crisps",
        {
            "id": "crisps-question",
            "type": "General",
            "answers": [
                {
                    "id": "crisps-answer",
                    "type": "Checkbox",
                    "options": [
                        {"label": "Ready salted", "value": "Ready salted"},
                        {"label": "Sweet chilli", "value": "Sweet chilli"},
                        {"label": "Cheese and onion", "value": "Cheese and onion"},
                    ],
                }
            ],
        },
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
    assert len(data_payload["answers"]) == 1
    assert data_payload["answers"][0].value == ["Ready salted", "Sweet chilli"]


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_radio_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(["radio-block"], section_id="section-1")]
    answers = AnswerStore([Answer("radio-answer", "Coffee").to_dict()])
    questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "radio-group",
        "radio-block",
        {
            "id": "radio-question",
            "type": "General",
            "answers": [
                {
                    "type": "Radio",
                    "id": "radio-answer",
                    "options": [
                        {"label": "Coffee", "value": "Coffee"},
                        {"label": "Tea", "value": "Tea"},
                    ],
                }
            ],
        },
    )

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

    assert len(data_payload["answers"]) == 1
    assert data_payload["answers"][0].value == "Coffee"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_number_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(["number-block"], section_id="section-1")]
    answers = AnswerStore([Answer("number-answer", 1.755).to_dict()])
    questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "number-group",
        "number-block",
        {
            "id": "number-question",
            "type": "General",
            "answers": [{"id": "number-answer", "type": "Number"}],
        },
    )

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

    assert len(data_payload["answers"]) == 1
    assert data_payload["answers"][0].value == 1.755


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_percentage_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(["percentage-block"], section_id="section-1")]
    answers = AnswerStore([Answer("percentage-answer", 99).to_dict()])
    questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "percentage-group",
        "percentage-block",
        {
            "id": "percentage-question",
            "type": "General",
            "answers": [{"id": "percentage-answer", "type": "Percentage"}],
        },
    )

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

    assert len(data_payload["answers"]) == 1
    assert data_payload["answers"][0].value == 99


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_textarea_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(["textarea-block"], section_id="section-1")]
    answers = AnswerStore(
        [Answer("textarea-answer", "This is an example text!").to_dict()]
    )
    questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "textarea-group",
        "textarea-block",
        {
            "id": "textarea-question",
            "type": "General",
            "answers": [{"id": "textarea-answer", "type": "TextArea"}],
        },
    )

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

    assert len(data_payload["answers"]) == 1
    assert data_payload["answers"][0].value == "This is an example text!"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_currency_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(["currency-block"], section_id="section-1")]
    answers = AnswerStore([Answer("currency-answer", 100).to_dict()])
    questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "currency-group",
        "currency-block",
        {
            "id": "currency-question",
            "type": "General",
            "answers": [{"id": "currency-answer", "type": "Currency"}],
        },
    )

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

    assert len(data_payload["answers"]) == 1
    assert data_payload["answers"][0].value == 100


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_dropdown_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(["dropdown-block"], section_id="section-1")]
    answers = AnswerStore([Answer("dropdown-answer", "Rugby is better!").to_dict()])
    questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "dropdown-group",
        "dropdown-block",
        {
            "id": "dropdown-question",
            "type": "General",
            "answers": [
                {
                    "id": "dropdown-answer",
                    "type": "Dropdown",
                    "options": [
                        {"label": "Liverpool", "value": "Liverpool"},
                        {"label": "Chelsea", "value": "Chelsea"},
                        {"label": "Rugby is better!", "value": "Rugby is better!"},
                    ],
                }
            ],
        },
    )

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
    assert len(data_payload["answers"]) == 1
    assert data_payload["answers"][0].value == "Rugby is better!"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_date_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(["date-block"], section_id="section-1")]
    answers = AnswerStore(
        [
            Answer("single-date-answer", "01-01-1990").to_dict(),
            Answer("month-year-answer", "01-1990").to_dict(),
        ]
    )
    questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "date-group",
        "date-block",
        {
            "id": "single-date-question",
            "type": "General",
            "answers": [{"id": "single-date-answer", "type": "Date"}],
        },
    )

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

    assert len(data_payload["answers"]) == 1

    assert data_payload["answers"][0].value == "01-01-1990"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_month_year_date_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(["date-block"], section_id="section-1")]
    answers = AnswerStore(
        [
            Answer("single-date-answer", "01-01-1990").to_dict(),
            Answer("month-year-answer", "01-1990").to_dict(),
        ]
    )
    questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "date-group",
        "date-block",
        {
            "id": "month-year-question",
            "type": "General",
            "answers": [{"id": "month-year-answer", "type": "MonthYearDate"}],
        },
    )

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

    assert len(data_payload["answers"]) == 1

    assert data_payload["answers"][0].value == "01-1990"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_unit_answer(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [RoutingPath(["unit-block"], section_id="section-1")]
    answers = AnswerStore([Answer("unit-answer", 10).to_dict()])
    questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "unit-group",
        "unit-block",
        {
            "id": "unit-question",
            "type": "General",
            "answers": [{"id": "unit-answer", "type": "Unit"}],
        },
    )

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

    assert len(data_payload["answers"]) == 1
    assert data_payload["answers"][0].value == 10


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_primary_person_list_item_conversion(version):
    questionnaire_store = get_questionnaire_store(version)

    routing_path = [
        RoutingPath(
            ["primary-person-list-collector", "list-collector"], section_id="section-1"
        )
    ]

    answer_objects = [
        {"answer_id": "you-live-here", "value": "Yes"},
        {"answer_id": "first-name", "value": "1", "list_item_id": "xJlKBy"},
        {"answer_id": "last-name", "value": "1", "list_item_id": "xJlKBy"},
        {"answer_id": "first-name", "value": "2", "list_item_id": "RfAGDc"},
        {"answer_id": "last-name", "value": "2", "list_item_id": "RfAGDc"},
        {"answer_id": "anyone-else", "value": "No"},
    ]

    answers = AnswerStore(answer_objects)

    list_store = ListStore(
        existing_items=[
            {
                "name": "people",
                "items": ["xJlKBy", "RfAGDc"],
                "primary_person": "xJlKBy",
            }
        ]
    )

    questionnaire_store.answer_store = answers
    questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_list_collector_primary_person")

    output = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    data_dict = json_loads(json_dumps(output["answers"]))

    assert sorted(answer_objects, key=lambda x: x["answer_id"]) == sorted(
        data_dict, key=lambda x: x["answer_id"]
    )


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_list_item_conversion(version):
    questionnaire_store = get_questionnaire_store(version)

    routing_path = [
        RoutingPath(
            ["list-collector", "next-interstitial", "another-list-collector-block"],
            section_id="section-1",
        )
    ]

    answer_objects = [
        {"answer_id": "first-name", "value": "1", "list_item_id": "xJlKBy"},
        {"answer_id": "last-name", "value": "1", "list_item_id": "xJlKBy"},
        {"answer_id": "first-name", "value": "2", "list_item_id": "RfAGDc"},
        {"answer_id": "last-name", "value": "2", "list_item_id": "RfAGDc"},
        {"answer_id": "anyone-else", "value": "No"},
        {"answer_id": "another-anyone-else", "value": "No"},
        {"answer_id": "extraneous-answer", "value": "Bad", "list_item_id": "123"},
    ]

    answers = AnswerStore(answer_objects)

    list_store = ListStore(
        existing_items=[{"name": "people", "items": ["xJlKBy", "RfAGDc"]}]
    )

    questionnaire_store.answer_store = answers
    questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_list_collector")

    output = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    del answer_objects[-1]

    data_dict = json_loads(json_dumps(output["answers"]))

    assert sorted(answer_objects, key=lambda x: x["answer_id"]) == sorted(
        data_dict, key=lambda x: x["answer_id"]
    )


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_list_item_conversion_empty_list(version):
    """Test that the list store is populated with an empty list for lists which
    do not have answers yet."""
    questionnaire_store = get_questionnaire_store(version)

    routing_path = [
        RoutingPath(
            ["list-collector", "next-interstitial", "another-list-collector-block"],
            section_id="section-1",
        )
    ]

    answer_objects = [
        {"answer_id": "last-name", "value": "2", "list_item_id": "RfAGDc"},
        {"answer_id": "anyone-else", "value": "No"},
        {"answer_id": "another-anyone-else", "value": "No"},
        {"answer_id": "extraneous-answer", "value": "Bad", "list_item_id": "123"},
    ]

    questionnaire_store.answer_store = AnswerStore(answer_objects)
    questionnaire_store.list_store = ListStore()

    schema = load_schema_from_name("test_list_collector")

    output = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    # Answers not on the routing path
    del answer_objects[0]
    del answer_objects[-1]

    data_dict = json_loads(json_dumps(output["answers"]))

    assert sorted(answer_objects, key=lambda x: x["answer_id"]) == sorted(
        data_dict, key=lambda x: x["answer_id"]
    )


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_default_answers_not_present_when_not_answered(version):
    """Test that default values aren't submitted downstream when an answer with
    a default value is not present in the answer store."""
    questionnaire_store = get_questionnaire_store(version)

    schema = load_schema_from_name("test_default")

    answer_objects = [{"answer_id": "number-question-two", "value": "12"}]

    questionnaire_store.answer_store = AnswerStore(answer_objects)
    questionnaire_store.list_store = ListStore()

    routing_path = [
        RoutingPath(
            ["number-question-one", "number-question-two"], section_id="default-section"
        )
    ]

    output = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    data = json_loads(json_dumps(output["answers"]))

    answer_ids = {answer["answer_id"] for answer in data}
    assert "answer-one" not in answer_ids


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_list_structure_in_payload_is_as_expected(version):
    questionnaire_store = get_questionnaire_store(version)

    routing_path = [
        RoutingPath(
            ["primary-person-list-collector", "list-collector"], section_id="section-1"
        )
    ]

    answer_objects = [
        {"answer_id": "you-live-here", "value": "Yes"},
        {"answer_id": "first-name", "value": "1", "list_item_id": "xJlKBy"},
        {"answer_id": "last-name", "value": "1", "list_item_id": "xJlKBy"},
        {"answer_id": "first-name", "value": "2", "list_item_id": "RfAGDc"},
        {"answer_id": "last-name", "value": "2", "list_item_id": "RfAGDc"},
        {"answer_id": "anyone-else", "value": "No"},
    ]

    answers = AnswerStore(answer_objects)

    list_store = ListStore(
        existing_items=[
            {
                "name": "people",
                "items": ["xJlKBy", "RfAGDc"],
                "primary_person": "xJlKBy",
            }
        ]
    )

    questionnaire_store.answer_store = answers
    questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_list_collector_primary_person")

    output = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    data_dict = json_loads(json_dumps(output["lists"]))

    assert data_dict[0]["name"] == "people"
    assert "xJlKBy" in data_dict[0]["items"]
    assert data_dict[0]["primary_person"] == "xJlKBy"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_primary_person_not_in_payload_when_not_answered(version):
    questionnaire_store = get_questionnaire_store(version)

    routing_path = [
        RoutingPath(
            ["list-collector", "next-interstitial", "another-list-collector-block"],
            section_id="section-1",
        )
    ]

    answer_objects = [
        {"answer_id": "first-name", "value": "1", "list_item_id": "xJlKBy"},
        {"answer_id": "last-name", "value": "1", "list_item_id": "xJlKBy"},
        {"answer_id": "first-name", "value": "2", "list_item_id": "RfAGDc"},
        {"answer_id": "last-name", "value": "2", "list_item_id": "RfAGDc"},
        {"answer_id": "anyone-else", "value": "No"},
        {"answer_id": "another-anyone-else", "value": "No"},
        {"answer_id": "extraneous-answer", "value": "Bad", "list_item_id": "123"},
    ]

    answers = AnswerStore(answer_objects)

    list_store = ListStore(
        existing_items=[{"name": "people", "items": ["xJlKBy", "RfAGDc"]}]
    )

    questionnaire_store.answer_store = answers
    questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_list_collector")

    output = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    data_dict = json_loads(json_dumps(output["lists"]))

    assert "primary_person" not in data_dict[0]


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_relationships_in_payload(version):
    questionnaire_store = get_questionnaire_store(version)

    routing_path = [
        RoutingPath(
            ["list-collector", "relationships"],
            section_id="section",
        )
    ]

    answer_objects = [
        {"answer_id": "first-name", "value": "1", "list_item_id": "person1"},
        {"answer_id": "last-name", "value": "1", "list_item_id": "person1"},
        {"answer_id": "first-name", "value": "2", "list_item_id": "person2"},
        {"answer_id": "last-name", "value": "2", "list_item_id": "person2"},
        {"answer_id": "first-name", "value": "3", "list_item_id": "person3"},
        {"answer_id": "last-name", "value": "3", "list_item_id": "person3"},
        {"answer_id": "anyone-else", "value": "No"},
        {
            "answer_id": "relationship-answer",
            "value": [
                {
                    "list_item_id": "person1",
                    "to_list_item_id": "person2",
                    "relationship": "Husband or Wife",
                },
                {
                    "list_item_id": "person1",
                    "to_list_item_id": "person3",
                    "relationship": "Son or daughter",
                },
            ],
        },
    ]

    answers = AnswerStore(answer_objects)

    list_store = ListStore(
        existing_items=[
            {
                "name": "people",
                "items": [
                    "person1",
                    "person2",
                    "person3",
                ],
            }
        ]
    )

    questionnaire_store.answer_store = answers
    questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_relationships")

    output = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    data = json_loads(json_dumps(output["answers"]))
    answers = {answer["answer_id"]: answer for answer in data}

    expected_relationships_answer = [
        {
            "list_item_id": "person1",
            "relationship": "Husband or Wife",
            "to_list_item_id": "person2",
        },
        {
            "list_item_id": "person1",
            "relationship": "Son or daughter",
            "to_list_item_id": "person3",
        },
    ]

    relationships_answer = answers["relationship-answer"]
    assert expected_relationships_answer == relationships_answer["value"]


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_no_relationships_in_payload(version):
    questionnaire_store = get_questionnaire_store(version)

    routing_path = [
        RoutingPath(
            ["list-collector", "relationships"],
            section_id="section",
        )
    ]

    answer_objects = [
        {"answer_id": "first-name", "value": "1", "list_item_id": "person1"},
        {"answer_id": "last-name", "value": "1", "list_item_id": "person1"},
        {"answer_id": "first-name", "value": "2", "list_item_id": "person2"},
        {"answer_id": "last-name", "value": "2", "list_item_id": "person2"},
        {"answer_id": "first-name", "value": "3", "list_item_id": "person3"},
        {"answer_id": "last-name", "value": "3", "list_item_id": "person3"},
        {"answer_id": "anyone-else", "value": "No"},
    ]

    answers = AnswerStore(answer_objects)

    list_store = ListStore(
        existing_items=[
            {
                "name": "people",
                "items": [
                    "person1",
                    "person2",
                    "person3",
                ],
            }
        ]
    )

    questionnaire_store.answer_store = answers
    questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_relationships_unrelated")

    output = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    data = json_loads(json_dumps(output["answers"]))
    answers = {answer["answer_id"]: answer for answer in data}

    assert "relationship-answer" not in answers


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_unrelated_block_answers_in_payload(version):
    questionnaire_store = get_questionnaire_store(version)

    routing_path = [
        RoutingPath(
            ["list-collector", "relationships"],
            section_id="section",
        )
    ]

    answer_objects = [
        {"answer_id": "first-name", "value": "1", "list_item_id": "person1"},
        {"answer_id": "last-name", "value": "1", "list_item_id": "person1"},
        {"answer_id": "first-name", "value": "2", "list_item_id": "person2"},
        {"answer_id": "last-name", "value": "2", "list_item_id": "person2"},
        {"answer_id": "first-name", "value": "3", "list_item_id": "person3"},
        {"answer_id": "last-name", "value": "3", "list_item_id": "person3"},
        {"answer_id": "first-name", "value": "4", "list_item_id": "person4"},
        {"answer_id": "last-name", "value": "4", "list_item_id": "person4"},
        {"answer_id": "first-name", "value": "5", "list_item_id": "person5"},
        {"answer_id": "last-name", "value": "5", "list_item_id": "person5"},
        {"answer_id": "anyone-else", "value": "No"},
        {
            "answer_id": "relationship-answer",
            "value": [
                {
                    "list_item_id": "person1",
                    "to_list_item_id": "person2",
                    "relationship": "Unrelated",
                },
                {
                    "list_item_id": "person1",
                    "to_list_item_id": "person3",
                    "relationship": "Unrelated",
                },
                {
                    "list_item_id": "person1",
                    "to_list_item_id": "person4",
                    "relationship": "Unrelated",
                },
            ],
        },
        {
            "answer_id": "related-to-anyone-else-answer",
            "value": "Yes",
            "list_item_id": "person1",
        },
    ]

    answers = AnswerStore(answer_objects)

    list_store = ListStore(
        existing_items=[
            {
                "name": "people",
                "items": [
                    "person1",
                    "person2",
                    "person3",
                    "person4",
                    "person5",
                ],
            }
        ]
    )

    questionnaire_store.answer_store = answers
    questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_relationships_unrelated")

    output = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    data = json_loads(json_dumps(output["answers"]))
    answers = {
        (answer["answer_id"], answer.get("list_item_id")): answer for answer in data
    }

    expected_relationships_answer = [
        {
            "list_item_id": "person1",
            "relationship": "Unrelated",
            "to_list_item_id": "person2",
        },
        {
            "list_item_id": "person1",
            "relationship": "Unrelated",
            "to_list_item_id": "person3",
        },
        {
            "list_item_id": "person1",
            "relationship": "Unrelated",
            "to_list_item_id": "person4",
        },
    ]

    assert ("related-to-anyone-else-answer", "person1") in answers
    relationships_answer = answers[("relationship-answer", None)]
    assert expected_relationships_answer == relationships_answer["value"]


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_unrelated_block_answers_not_on_path_not_in_payload(version):
    questionnaire_store = get_questionnaire_store(version)

    routing_path = [
        RoutingPath(
            ["list-collector", "relationships"],
            section_id="section",
        )
    ]

    answer_objects = [
        {"answer_id": "first-name", "value": "1", "list_item_id": "person1"},
        {"answer_id": "last-name", "value": "1", "list_item_id": "person1"},
        {"answer_id": "first-name", "value": "2", "list_item_id": "person2"},
        {"answer_id": "last-name", "value": "2", "list_item_id": "person2"},
        {"answer_id": "first-name", "value": "3", "list_item_id": "person3"},
        {"answer_id": "last-name", "value": "3", "list_item_id": "person3"},
        {"answer_id": "first-name", "value": "4", "list_item_id": "person4"},
        {"answer_id": "last-name", "value": "4", "list_item_id": "person4"},
        {"answer_id": "first-name", "value": "5", "list_item_id": "person5"},
        {"answer_id": "last-name", "value": "5", "list_item_id": "person5"},
        {"answer_id": "anyone-else", "value": "No"},
        {
            "answer_id": "relationship-answer",
            "value": [
                {
                    "list_item_id": "person1",
                    "to_list_item_id": "person2",
                    "relationship": "Unrelated",
                },
                {
                    "list_item_id": "person1",
                    "to_list_item_id": "person3",
                    "relationship": "Related",
                },
            ],
        },
        {
            "answer_id": "related-to-anyone-else-answer",
            "value": "No",
            "list_item_id": "person1",
        },
    ]

    answers = AnswerStore(answer_objects)

    list_store = ListStore(
        existing_items=[
            {
                "name": "people",
                "items": [
                    "person1",
                    "person2",
                    "person3",
                    "person4",
                    "person5",
                ],
            }
        ]
    )

    questionnaire_store.answer_store = answers
    questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_relationships_unrelated")

    output = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    data = json_loads(json_dumps(output["answers"]))
    answers = {
        (answer["answer_id"], answer.get("list_item_id")): answer for answer in data
    }

    assert ("related-to-anyone-else-answer", "person1") not in answers


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_relationship_answers_not_on_path_in_payload(version):
    questionnaire_store = get_questionnaire_store(version)

    routing_path = [
        RoutingPath(
            ["list-collector", "relationships"],
            section_id="section",
        )
    ]

    answer_objects = [
        {"answer_id": "first-name", "value": "1", "list_item_id": "person1"},
        {"answer_id": "last-name", "value": "1", "list_item_id": "person1"},
        {"answer_id": "first-name", "value": "2", "list_item_id": "person2"},
        {"answer_id": "last-name", "value": "2", "list_item_id": "person2"},
        {"answer_id": "first-name", "value": "3", "list_item_id": "person3"},
        {"answer_id": "last-name", "value": "3", "list_item_id": "person3"},
        {"answer_id": "first-name", "value": "4", "list_item_id": "person4"},
        {"answer_id": "last-name", "value": "4", "list_item_id": "person4"},
        {"answer_id": "first-name", "value": "5", "list_item_id": "person5"},
        {"answer_id": "last-name", "value": "5", "list_item_id": "person5"},
        {"answer_id": "anyone-else", "value": "No"},
        {
            "answer_id": "relationship-answer",
            "value": [
                {
                    "list_item_id": "person1",
                    "to_list_item_id": "person2",
                    "relationship": "Unrelated",
                },
                {
                    "list_item_id": "person1",
                    "to_list_item_id": "person3",
                    "relationship": "Unrelated",
                },
                {
                    "list_item_id": "person1",
                    "to_list_item_id": "person4",
                    "relationship": "Unrelated",
                },
                {
                    "list_item_id": "person1",
                    "to_list_item_id": "person5",
                    "relationship": "Unrelated",
                },
            ],
        },
        {
            "answer_id": "related-to-anyone-else-answer",
            "value": "No",
            "list_item_id": "person1",
        },
    ]

    answers = AnswerStore(answer_objects)

    list_store = ListStore(
        existing_items=[
            {
                "name": "people",
                "items": [
                    "person1",
                    "person2",
                    "person3",
                    "person4",
                    "person5",
                ],
            }
        ]
    )

    questionnaire_store.answer_store = answers
    questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_relationships_unrelated")

    output = get_payload_data(
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        schema,
        routing_path,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
        questionnaire_store.progress_store,
        questionnaire_store.supplementary_data_store,
    )

    data = json_loads(json_dumps(output["answers"]))
    answers = {
        (answer["answer_id"], answer.get("list_item_id")): answer for answer in data
    }

    expected_relationships_answer = [
        {
            "list_item_id": "person1",
            "relationship": "Unrelated",
            "to_list_item_id": "person2",
        },
        {
            "list_item_id": "person1",
            "relationship": "Unrelated",
            "to_list_item_id": "person3",
        },
        {
            "list_item_id": "person1",
            "relationship": "Unrelated",
            "to_list_item_id": "person4",
        },
        {
            "list_item_id": "person1",
            "relationship": "Unrelated",
            "to_list_item_id": "person5",
        },
    ]

    assert ("related-to-anyone-else-answer", "person1") in answers
    relationships_answer = answers[("relationship-answer", None)]
    assert expected_relationships_answer == relationships_answer["value"]


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_answers_codes_only_present_for_answered_questions(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(["mandatory-checkbox", "name-block"], section_id="default-section")
    ]

    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("name-answer", "Joe Bloggs", None).to_dict(),
        ]
    )

    schema = load_schema_from_name("test_answer_codes")

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
    assert len(data_payload["answer_codes"]) == 1
    assert data_payload["answer_codes"][0]["answer_id"] == "name-answer"
    assert data_payload["answer_codes"][0]["code"] == "2"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_all_answers_codes_for_answer_options_in_payload_when_one_is_answered(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(["mandatory-checkbox"], section_id="default-section")
    ]

    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("mandatory-checkbox-answer", ["Ham"]).to_dict(),
        ]
    )

    schema = load_schema_from_name("test_answer_codes")

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
    assert len(data_payload["answer_codes"]) == 5
    assert all(
        answer_code["answer_id"] == "mandatory-checkbox-answer"
        for answer_code in data_payload["answer_codes"]
    )


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_no_answers_codes_in_payload_when_no_questions_answered(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(["mandatory-checkbox"], section_id="default-section")
    ]

    questionnaire_store.answer_store = AnswerStore()

    schema = load_schema_from_name("test_answer_codes")

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
    assert "answer_codes" not in data_payload


@pytest.mark.parametrize(
    "version",
    (AuthPayloadVersion.V2, None),
)
def test_payload_dynamic_answers(version):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(
            ["any-supermarket", "list-collector", "dynamic-answer"],
            section_id="section",
        )
    ]

    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("any-supermarket-answer", "Yes", None).to_dict(),
            Answer("supermarket-name", "Tesco", "tUJzGV").to_dict(),
            Answer("supermarket-name", "Aldi", "vhECeh").to_dict(),
            Answer("list-collector-answer", "No", None).to_dict(),
            Answer("percentage-of-shopping", 12, "tUJzGV").to_dict(),
            Answer("percentage-of-shopping", 21, "vhECeh").to_dict(),
        ]
    )

    questionnaire_store.list_store = ListStore(
        [{"items": ["tUJzGV", "vhECeh"], "name": "supermarkets"}]
    )

    schema = load_schema_from_name("test_dynamic_answers_list_source")

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
    assert (
        Answer(answer_id="percentage-of-shopping", value=12, list_item_id="tUJzGV")
        in data_payload["answers"]
    )
    assert (
        Answer(answer_id="percentage-of-shopping", value=21, list_item_id="vhECeh")
        in data_payload["answers"]
    )


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_repeating_block_answers_present(
    version, repeating_blocks_answer_store, repeating_blocks_list_store
):
    questionnaire_store = get_questionnaire_store(version)

    full_routing_path = [
        RoutingPath(
            [
                "responsible-party",
                "any-companies-or-branches",
                "any-other-companies-or-branches",
                "any-other-trading-details",
            ],
            section_id="section-companies",
        )
    ]

    questionnaire_store.answer_store = repeating_blocks_answer_store
    questionnaire_store.list_store = repeating_blocks_list_store

    schema = load_schema_from_name(
        "test_list_collector_repeating_blocks_section_summary"
    )

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

    expected_answer_codes = [
        {"answer_id": "responsible-party-answer", "code": "1"},
        {"answer_id": "any-companies-or-branches-answer", "code": "2"},
        {"answer_id": "company-or-branch-name", "code": "2a"},
        {"answer_id": "registration-number", "code": "2b"},
        {"answer_id": "registration-date", "code": "2c"},
        {"answer_id": "authorised-trader-uk-radio", "code": "2d"},
        {"answer_id": "authorised-trader-eu-radio", "code": "2e"},
    ]

    expected_answers = [
        {"answer_id": "responsible-party-answer", "value": "Yes"},
        {"answer_id": "any-companies-or-branches-answer", "value": "Yes"},
        {
            "answer_id": "company-or-branch-name",
            "value": "CompanyA",
            "list_item_id": "PlwgoG",
        },
        {
            "answer_id": "registration-number",
            "value": "123",
            "list_item_id": "PlwgoG",
        },
        {
            "answer_id": "registration-date",
            "value": "2023-01-01",
            "list_item_id": "PlwgoG",
        },
        {
            "answer_id": "authorised-trader-uk-radio",
            "value": "Yes",
            "list_item_id": "PlwgoG",
        },
        {
            "answer_id": "authorised-trader-eu-radio",
            "value": "Yes",
            "list_item_id": "PlwgoG",
        },
        {
            "answer_id": "company-or-branch-name",
            "value": "CompanyB",
            "list_item_id": "UHPLbX",
        },
        {
            "answer_id": "registration-number",
            "value": "456",
            "list_item_id": "UHPLbX",
        },
        {
            "answer_id": "registration-date",
            "value": "2023-01-01",
            "list_item_id": "UHPLbX",
        },
        {
            "answer_id": "authorised-trader-uk-radio",
            "value": "No",
            "list_item_id": "UHPLbX",
        },
        {
            "answer_id": "authorised-trader-eu-radio",
            "value": "No",
            "list_item_id": "UHPLbX",
        },
    ]

    answers_dict = json_loads(json_dumps(data_payload["answers"]))
    answer_codes_dict = json_loads(json_dumps(data_payload["answer_codes"]))

    assert answers_dict == expected_answers
    assert answer_codes_dict == expected_answer_codes


def test_payload_supplementary_data():
    questionnaire_store = get_questionnaire_store(AuthPayloadVersion.V2)

    full_routing_path = [
        RoutingPath(
            ["dynamic-answer"],
            section_id="section",
        )
    ]

    supplementary_data = {
        "schema_version": "v1",
        "identifier": "12346789012A",
        "note": {"title": "supermarket test survey", "description": "test data"},
        "items": {
            "supermarkets": [
                {"identifier": "123", "name": "Tesco"},
                {"identifier": "456", "name": "Aldi"},
            ]
        },
    }
    supermarkets_list_mappings = [
        {"identifier": "123", "list_item_id": "tUJzGV"},
        {"identifier": "456", "list_item_id": "vhECeh"},
    ]

    list_item_ids = ["tUJzGV", "vhECeh"]
    questionnaire_store.supplementary_data_store = SupplementaryDataStore(
        supplementary_data=supplementary_data,
        list_mappings={"supermarkets": supermarkets_list_mappings},
    )
    questionnaire_store.list_store = ListStore(
        [{"items": list_item_ids, "name": "supermarkets"}]
    )
    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("percentage-of-shopping", 12, list_item_ids[0]).to_dict(),
            Answer("percentage-of-shopping", 21, list_item_ids[1]).to_dict(),
        ]
    )

    schema = load_schema_from_name("test_supplementary_data")

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

    assert "supplementary_data" in data_payload
    assert "lists" in data_payload
    assert data_payload["supplementary_data"] == make_immutable(supplementary_data)
    assert len(data_payload["lists"]) == 1
    assert data_payload["lists"][0] == {
        "items": list_item_ids,
        "name": "supermarkets",
        "supplementary_data_mappings": make_immutable(supermarkets_list_mappings),
    }
