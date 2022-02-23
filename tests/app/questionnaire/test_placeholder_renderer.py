import pytest

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.questionnaire.placeholder_renderer import PlaceholderRenderer


def test_correct_pointers(pointers):
    assert pointers[0] == "/answers/0/options/0/label"


def test_renders_pointer(question_json, mocker):
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

    json_to_render = question_json.copy()
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
        question_json, "/answers/0/options/0/label", list_item_id=None
    )

    assert rendered == "Hal Abelson’s age is 28 years. Is this correct?"


def test_renders_json(question_json, mocker):
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
    json_to_render = question_json.copy()
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


def test_renders_json_uses_language(question_json, mocker):
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
    json_to_render = question_json.copy()
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


def test_errors_on_invalid_pointer(question_json, mocker):
    renderer = get_placeholder_render(mocker=mocker)

    with pytest.raises(ValueError):
        renderer.render_pointer(question_json, "/title", list_item_id=None)


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
