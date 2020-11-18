import simplejson as json

from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.routing_path import RoutingPath
from app.submitter.converter import convert_answers
from app.utilities.schema import load_schema_from_name
from tests.app.submitter.schema import make_schema


def test_convert_answers_to_payload_0_0_3(fake_questionnaire_store):
    full_routing_path = [
        RoutingPath(["about you", "where you live"], section_id="household-section")
    ]

    fake_questionnaire_store.answer_store = AnswerStore(
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
    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )

    # Then
    assert len(answer_object["data"]["answers"]) == 2
    assert answer_object["data"]["answers"][0].value == "Joe Bloggs"
    assert answer_object["data"]["answers"][1].value, "62 Somewhere"


def test_convert_payload_0_0_3_multiple_answers(fake_questionnaire_store):
    full_routing_path = [RoutingPath(["crisps"], section_id="section-1")]
    answers = AnswerStore(
        [Answer("crisps-answer", ["Ready salted", "Sweet chilli"]).to_dict()]
    )
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "favourite-food",
        "crisps",
        {
            "id": "crisps-question",
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
    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )
    # Then
    assert len(answer_object["data"]["answers"]) == 1
    assert answer_object["data"]["answers"][0].value == ["Ready salted", "Sweet chilli"]


def test_radio_answer(fake_questionnaire_store):
    full_routing_path = [RoutingPath(["radio-block"], section_id="section-1")]
    answers = AnswerStore([Answer("radio-answer", "Coffee").to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "radio-group",
        "radio-block",
        {
            "id": "radio-question",
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

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )

    assert len(answer_object["data"]["answers"]) == 1
    assert answer_object["data"]["answers"][0].value == "Coffee"


def test_number_answer(fake_questionnaire_store):
    full_routing_path = [RoutingPath(["number-block"], section_id="section-1")]
    answers = AnswerStore([Answer("number-answer", 1.755).to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "number-group",
        "number-block",
        {
            "id": "number-question",
            "answers": [{"id": "number-answer", "type": "Number"}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )

    assert len(answer_object["data"]["answers"]) == 1
    assert answer_object["data"]["answers"][0].value == 1.755


def test_percentage_answer(fake_questionnaire_store):
    full_routing_path = [RoutingPath(["percentage-block"], section_id="section-1")]
    answers = AnswerStore([Answer("percentage-answer", 99).to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "percentage-group",
        "percentage-block",
        {
            "id": "percentage-question",
            "answers": [{"id": "percentage-answer", "type": "Percentage"}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )

    assert len(answer_object["data"]["answers"]) == 1
    assert answer_object["data"]["answers"][0].value == 99


def test_textarea_answer(fake_questionnaire_store):
    full_routing_path = [RoutingPath(["textarea-block"], section_id="section-1")]
    answers = AnswerStore(
        [Answer("textarea-answer", "This is an example text!").to_dict()]
    )
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "textarea-group",
        "textarea-block",
        {
            "id": "textarea-question",
            "answers": [{"id": "textarea-answer", "type": "TextArea"}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )

    assert len(answer_object["data"]["answers"]) == 1
    assert answer_object["data"]["answers"][0].value == "This is an example text!"


def test_currency_answer(fake_questionnaire_store):
    full_routing_path = [RoutingPath(["currency-block"], section_id="section-1")]
    answers = AnswerStore([Answer("currency-answer", 100).to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "currency-group",
        "currency-block",
        {
            "id": "currency-question",
            "answers": [{"id": "currency-answer", "type": "Currency"}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )

    assert len(answer_object["data"]["answers"]) == 1
    assert answer_object["data"]["answers"][0].value == 100


def test_dropdown_answer(fake_questionnaire_store):
    full_routing_path = [RoutingPath(["dropdown-block"], section_id="section-1")]
    answers = AnswerStore([Answer("dropdown-answer", "Rugby is better!").to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "dropdown-group",
        "dropdown-block",
        {
            "id": "dropdown-question",
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

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )

    # Then
    assert len(answer_object["data"]["answers"]) == 1
    assert answer_object["data"]["answers"][0].value == "Rugby is better!"


def test_date_answer(fake_questionnaire_store):
    full_routing_path = [RoutingPath(["date-block"], section_id="section-1")]
    answers = AnswerStore(
        [
            Answer("single-date-answer", "01-01-1990").to_dict(),
            Answer("month-year-answer", "01-1990").to_dict(),
        ]
    )
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "date-group",
        "date-block",
        {
            "id": "single-date-question",
            "answers": [{"id": "single-date-answer", "type": "Date"}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )

    assert len(answer_object["data"]["answers"]) == 1

    assert answer_object["data"]["answers"][0].value == "01-01-1990"


def test_month_year_date_answer(fake_questionnaire_store):
    full_routing_path = [RoutingPath(["date-block"], section_id="section-1")]
    answers = AnswerStore(
        [
            Answer("single-date-answer", "01-01-1990").to_dict(),
            Answer("month-year-answer", "01-1990").to_dict(),
        ]
    )
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "date-group",
        "date-block",
        {
            "id": "month-year-question",
            "answers": [{"id": "month-year-answer", "type": "MonthYearDate"}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )

    assert len(answer_object["data"]["answers"]) == 1

    assert answer_object["data"]["answers"][0].value == "01-1990"


def test_unit_answer(fake_questionnaire_store):
    full_routing_path = [RoutingPath(["unit-block"], section_id="section-1")]
    answers = AnswerStore([Answer("unit-answer", 10).to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        "0.0.3",
        "section-1",
        "unit-group",
        "unit-block",
        {"id": "unit-question", "answers": [{"id": "unit-answer", "type": "Unit"}]},
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )

    assert len(answer_object["data"]["answers"]) == 1
    assert answer_object["data"]["answers"][0].value == 10


def test_primary_person_list_item_conversion(fake_questionnaire_store):
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

    fake_questionnaire_store.answer_store = answers
    fake_questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_list_collector_primary_person")

    output = convert_answers(schema, fake_questionnaire_store, routing_path)

    data_dict = json.loads(json.dumps(output["data"]["answers"], for_json=True))

    assert sorted(answer_objects, key=lambda x: x["answer_id"]) == sorted(
        data_dict, key=lambda x: x["answer_id"]
    )


def test_list_item_conversion(fake_questionnaire_store):
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

    fake_questionnaire_store.answer_store = answers
    fake_questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_list_collector")

    output = convert_answers(schema, fake_questionnaire_store, routing_path)

    del answer_objects[-1]

    data_dict = json.loads(json.dumps(output["data"]["answers"], for_json=True))

    assert sorted(answer_objects, key=lambda x: x["answer_id"]) == sorted(
        data_dict, key=lambda x: x["answer_id"]
    )


def test_list_item_conversion_empty_list(fake_questionnaire_store):
    """Test that the list store is populated with an empty list for lists which
    do not have answers yet."""
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

    fake_questionnaire_store.answer_store = AnswerStore(answer_objects)
    fake_questionnaire_store.list_store = ListStore()

    schema = load_schema_from_name("test_list_collector")

    output = convert_answers(schema, fake_questionnaire_store, routing_path)

    # Answers not on the routing path
    del answer_objects[0]
    del answer_objects[-1]

    data_dict = json.loads(json.dumps(output["data"]["answers"], for_json=True))

    assert sorted(answer_objects, key=lambda x: x["answer_id"]) == sorted(
        data_dict, key=lambda x: x["answer_id"]
    )


def test_default_answers_not_present_when_not_answered(fake_questionnaire_store):
    """Test that default values aren't submitted downstream when an answer with
    a default value is not present in the answer store."""
    schema = load_schema_from_name("test_default")

    answer_objects = [{"answer_id": "number-question-two", "value": "12"}]

    fake_questionnaire_store.answer_store = AnswerStore(answer_objects)
    fake_questionnaire_store.list_store = ListStore()

    routing_path = [
        RoutingPath(
            ["number-question-one", "number-question-two"], section_id="default-section"
        )
    ]

    output = convert_answers(schema, fake_questionnaire_store, routing_path)
    data = json.loads(json.dumps(output["data"]["answers"], for_json=True))

    answer_ids = {answer["answer_id"] for answer in data}
    assert "answer-one" not in answer_ids


def test_list_structure_in_payload_is_as_expected(fake_questionnaire_store):
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

    fake_questionnaire_store.answer_store = answers
    fake_questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_list_collector_primary_person")

    output = convert_answers(schema, fake_questionnaire_store, routing_path)

    data_dict = json.loads(json.dumps(output["data"]["lists"], for_json=True))

    assert data_dict[0]["name"] == "people"
    assert "xJlKBy" in data_dict[0]["items"]
    assert data_dict[0]["primary_person"] == "xJlKBy"


def test_primary_person_not_in_payload_when_not_answered(fake_questionnaire_store):
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

    fake_questionnaire_store.answer_store = answers
    fake_questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_list_collector")

    output = convert_answers(schema, fake_questionnaire_store, routing_path)

    data_dict = json.loads(json.dumps(output["data"]["lists"], for_json=True))

    assert "primary_person" not in data_dict[0]


def test_relationships_in_payload(fake_questionnaire_store):
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

    fake_questionnaire_store.answer_store = answers
    fake_questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_relationships")

    output = convert_answers(schema, fake_questionnaire_store, routing_path)
    data = json.loads(json.dumps(output["data"]["answers"], for_json=True))
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


def test_no_relationships_in_payload(fake_questionnaire_store):
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

    fake_questionnaire_store.answer_store = answers
    fake_questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_relationships_unrelated")

    output = convert_answers(schema, fake_questionnaire_store, routing_path)
    data = json.loads(json.dumps(output["data"]["answers"], for_json=True))
    answers = {answer["answer_id"]: answer for answer in data}

    assert "relationship-answer" not in answers


def test_unrelated_block_answers_in_payload(fake_questionnaire_store):
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

    fake_questionnaire_store.answer_store = answers
    fake_questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_relationships_unrelated")

    output = convert_answers(schema, fake_questionnaire_store, routing_path)
    data = json.loads(json.dumps(output["data"]["answers"], for_json=True))
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


def test_unrelated_block_answers_not_on_path_not_in_payload(fake_questionnaire_store):
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

    fake_questionnaire_store.answer_store = answers
    fake_questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_relationships_unrelated")

    output = convert_answers(schema, fake_questionnaire_store, routing_path)
    data = json.loads(json.dumps(output["data"]["answers"], for_json=True))
    answers = {
        (answer["answer_id"], answer.get("list_item_id")): answer for answer in data
    }

    assert ("related-to-anyone-else-answer", "person1") not in answers


def test_relationship_answers_not_on_path_in_payload(fake_questionnaire_store):
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

    fake_questionnaire_store.answer_store = answers
    fake_questionnaire_store.list_store = list_store

    schema = load_schema_from_name("test_relationships_unrelated")

    output = convert_answers(schema, fake_questionnaire_store, routing_path)
    data = json.loads(json.dumps(output["data"]["answers"], for_json=True))
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
