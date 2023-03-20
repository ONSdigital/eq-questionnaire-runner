import pytest

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer


def test_correct_pointers(placholder_transform_pointers):
    assert placholder_transform_pointers[0] == "/answers/0/options/0/label"


def test_renders_pointer(placholder_transform_question_json, mocker):
    mock_transform = {
        "transform": "calculate_date_difference",
        "arguments": {
            "first_date": {
                "source": "answers",
                "identifier": "date-of-birth-answer",
            },
            "second_date": {"value": "2019-02-01"},
        },
    }

    json_to_render = placholder_transform_question_json.copy()
    json_to_render["answers"][0]["options"][0]["label"]["placeholders"][1][
        "transforms"
    ][0] = mock_transform

    answer_store = AnswerStore(
        [
            {"answer_id": "first-name", "value": "Hal"},
            {"answer_id": "last-name", "value": "Abelson"},
            {"answer_id": "date-of-birth-answer", "value": "1991-01-01"},
        ]
    )
    renderer = get_placeholder_render(mocker=mocker, answer_store=answer_store)
    rendered = renderer.render_pointer(
        placholder_transform_question_json,
        "/answers/0/options/0/label",
        list_item_id=None,
    )

    assert rendered == "Hal Abelson’s age is 28 years. Is this correct?"


def test_renders_json(placholder_transform_question_json, mocker):
    mock_transform = {
        "transform": "calculate_date_difference",
        "arguments": {
            "first_date": {
                "source": "answers",
                "identifier": "date-of-birth-answer",
            },
            "second_date": {"value": "2019-02-01"},
        },
    }
    json_to_render = placholder_transform_question_json.copy()
    json_to_render["answers"][0]["options"][0]["label"]["placeholders"][1][
        "transforms"
    ][0] = mock_transform

    answer_store = AnswerStore(
        [
            {"answer_id": "first-name", "value": "Alfred"},
            {"answer_id": "last-name", "value": "Aho"},
            {"answer_id": "date-of-birth-answer", "value": "1986-01-01"},
        ]
    )

    renderer = get_placeholder_render(mocker=mocker, answer_store=answer_store)
    rendered_schema = renderer.render(json_to_render, list_item_id=None)
    rendered_label = rendered_schema["answers"][0]["options"][0]["label"]

    assert rendered_label == "Alfred Aho’s age is 33 years. Is this correct?"


def test_renders_json_dynamic_answers(
    placeholder_transform_question_dynamic_answers_json,
):
    json_to_render = placeholder_transform_question_dynamic_answers_json

    answer_store = AnswerStore(
        [
            {"answer_id": "mandatory-checkbox-answer", "value": ["Tesco", "Aldi"]},
        ]
    )

    renderer = get_placeholder_render_dynamic_answers(answer_store=answer_store)
    rendered_schema = renderer.render(json_to_render, list_item_id=None)
    rendered_label_first = rendered_schema["answers"][0]["label"]
    rendered_id_first = rendered_schema["answers"][0]["id"]
    rendered_label_second = rendered_schema["answers"][1]["label"]
    rendered_id_second = rendered_schema["answers"][1]["id"]

    assert rendered_label_first == "Percentage of shopping at Tesco"
    assert rendered_id_first == "percentage-of-shopping-tesco"
    assert rendered_label_second == "Percentage of shopping at Aldi"
    assert rendered_id_second == "percentage-of-shopping-aldi"


def test_renders_json_uses_language(placholder_transform_question_json, mocker):
    mock_transform = {
        "transform": "calculate_date_difference",
        "arguments": {
            "first_date": {
                "source": "answers",
                "identifier": "date-of-birth-answer",
            },
            "second_date": {"value": "2019-02-01"},
        },
    }
    json_to_render = placholder_transform_question_json.copy()
    json_to_render["answers"][0]["options"][0]["label"]["placeholders"][1][
        "transforms"
    ][0] = mock_transform

    answer_store = AnswerStore(
        [
            {"answer_id": "first-name", "value": "Alfred"},
            {"answer_id": "last-name", "value": "Aho"},
            {"answer_id": "date-of-birth-answer", "value": "1986-01-01"},
        ]
    )
    renderer = get_placeholder_render(
        mocker=mocker, language="cy", answer_store=answer_store
    )
    rendered_schema = renderer.render(json_to_render, list_item_id=None)
    rendered_label = rendered_schema["answers"][0]["options"][0]["label"]

    assert rendered_label == "Alfred Aho age is 33 years. Is this correct?"


def test_errors_on_invalid_pointer(placholder_transform_question_json, mocker):
    renderer = get_placeholder_render(mocker=mocker)

    with pytest.raises(ValueError):
        renderer.render_pointer(
            placholder_transform_question_json, "/title", list_item_id=None
        )


def test_errors_on_invalid_json(mocker):
    renderer = get_placeholder_render(mocker=mocker)
    with pytest.raises(ValueError):
        dict_to_render = {"invalid": {"no": "placeholders", "in": "this"}}
        renderer.render_pointer(dict_to_render, "/invalid", list_item_id=None)


def test_renders_text_plural_from_answers(mocker):
    answer_store = AnswerStore([{"answer_id": "number-of-people", "value": 1}])
    renderer = get_placeholder_render(mocker=mocker, answer_store=answer_store)
    rendered_text = renderer.render_placeholder(
        {
            "text_plural": {
                "forms": {
                    "one": "Yes, {number_of_people} person lives here",
                    "other": "Yes, {number_of_people} people live here",
                },
                "count": {"source": "answers", "identifier": "number-of-people"},
            },
            "placeholders": [
                {
                    "placeholder": "number_of_people",
                    "value": {"source": "answers", "identifier": "number-of-people"},
                }
            ],
        },
        None,
    )

    assert rendered_text == "Yes, 1 person lives here"


def test_renders_text_plural_from_list(mocker):
    renderer = get_placeholder_render(mocker=mocker)

    rendered_text = renderer.render_placeholder(
        {
            "text_plural": {
                "forms": {
                    "one": "Yes, {number_of_people} person lives here",
                    "other": "Yes, {number_of_people} people live here",
                },
                "count": {"source": "list", "identifier": "household"},
            },
            "placeholders": [
                {
                    "placeholder": "number_of_people",
                    "value": {
                        "source": "list",
                        "identifier": "household",
                        "selector": "count",
                    },
                }
            ],
        },
        None,
    )

    assert rendered_text == "Yes, 0 people live here"


def test_renders_text_plural_from_metadata(mocker):
    metadata = {"some_value": 100}
    renderer = get_placeholder_render(mocker=mocker, metadata=metadata)

    rendered_text = renderer.render_placeholder(
        {
            "text_plural": {
                "forms": {
                    "one": "Yes, {number_of_people} person lives here",
                    "other": "Yes, {number_of_people} people live here",
                },
                "count": {"source": "metadata", "identifier": "some_value"},
            },
            "placeholders": [
                {
                    "placeholder": "number_of_people",
                    "value": {"source": "metadata", "identifier": "some_value"},
                }
            ],
        },
        None,
    )

    assert rendered_text == "Yes, 100 people live here"


def get_placeholder_render(
    *,
    language="en",
    answer_store=AnswerStore(),
    list_store=ListStore(),
    metadata=None,
    response_metadata=None,
    mocker,
):
    renderer = PlaceholderRenderer(
        language=language,
        answer_store=answer_store,
        list_store=list_store,
        metadata=metadata or {},
        response_metadata=response_metadata or {},
        schema=mocker.Mock(),
    )
    return renderer


def get_placeholder_render_dynamic_answers(
    *,
    language="en",
    answer_store=AnswerStore(),
    list_store=ListStore(),
    metadata=None,
    response_metadata=None,
):
    renderer = PlaceholderRenderer(
        language=language,
        answer_store=answer_store,
        list_store=list_store,
        metadata=metadata or {},
        response_metadata=response_metadata or {},
        schema=QuestionnaireSchema(
            {
                "sections": [
                    {
                        "id": "default-section",
                        "groups": [
                            {
                                "blocks": [
                                    {
                                        "type": "Question",
                                        "id": "mandatory-checkbox",
                                        "question": {
                                            "answers": [
                                                {
                                                    "id": "mandatory-checkbox-answer",
                                                    "mandatory": True,
                                                    "options": [
                                                        {
                                                            "label": "Tesco",
                                                            "value": "Tesco",
                                                        },
                                                        {
                                                            "label": "Aldi",
                                                            "value": "Aldi",
                                                        },
                                                    ],
                                                    "type": "Checkbox",
                                                }
                                            ],
                                            "id": "mandatory-checkbox-question",
                                            "title": "Which supermarkets do you use for your weekly shopping?",
                                            "type": "General",
                                        },
                                    },
                                    {
                                        "type": "Question",
                                        "id": "non-mandatory-checkbox",
                                        "question": {
                                            "dynamic_answers": {
                                                "values": {
                                                    "source": "answers",
                                                    "identifier": "mandatory-checkbox-answer",
                                                },
                                                "answers": [
                                                    {
                                                        "label": {
                                                            "text": "Percentage of shopping at {transformed_value}",
                                                            "placeholders": [
                                                                {
                                                                    "placeholder": "transformed_value",
                                                                    "transforms": [
                                                                        {
                                                                            "transform": "option_label_from_value",
                                                                            "arguments": {
                                                                                "value": "self",
                                                                                "answer_id": "mandatory-checkbox-answer",
                                                                            },
                                                                        }
                                                                    ],
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
                                            "answers": [],
                                            "id": "non-mandatory-checkbox-question",
                                            "title": "What percent of your shopping do you do at each of the following supermarket?",
                                            "type": "General",
                                        },
                                    },
                                ],
                                "id": "checkboxes",
                            }
                        ],
                    }
                ]
            }
        ),
    )
    return renderer
