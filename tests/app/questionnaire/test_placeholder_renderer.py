import pytest
from mock import MagicMock

from app.data_models import ProgressStore
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.questionnaire import Location
from app.questionnaire.placeholder_parser import PlaceholderParser
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.utilities.schema import load_schema_from_name


def test_correct_pointers(placholder_transform_pointers):
    assert placholder_transform_pointers[0] == "/answers/0/options/0/label"


def test_renders_pointer(
    placholder_transform_question_json, mock_schema, mock_renderer, mock_location
):
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

    renderer = get_placeholder_render(answer_store=answer_store)
    rendered = renderer.render_pointer(
        dict_to_render=placholder_transform_question_json,
        pointer_to_render="/answers/0/options/0/label",
        list_item_id=None,
        placeholder_parser=PlaceholderParser(
            language="en",
            answer_store=answer_store,
            list_store=ListStore(),
            metadata=None,
            response_metadata={},
            schema=mock_schema,
            location=mock_location,
            renderer=mock_renderer,
            progress_store=ProgressStore(),
        ),
    )

    assert rendered == "Hal Abelson’s age is 28 years. Is this correct?"


def test_renders_json(placholder_transform_question_json):
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

    renderer = get_placeholder_render(answer_store=answer_store)
    rendered_schema = renderer.render(data_to_render=json_to_render, list_item_id=None)
    rendered_label = rendered_schema["answers"][0]["options"][0]["label"]

    assert rendered_label == "Alfred Aho’s age is 33 years. Is this correct?"


def test_renders_json_uses_language(placholder_transform_question_json):
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

    renderer = get_placeholder_render(language="cy", answer_store=answer_store)
    rendered_schema = renderer.render(data_to_render=json_to_render, list_item_id=None)
    rendered_label = rendered_schema["answers"][0]["options"][0]["label"]

    assert rendered_label == "Alfred Aho age is 33 years. Is this correct?"


def test_errors_on_invalid_pointer(placholder_transform_question_json, mock_schema):
    renderer = get_placeholder_render()

    with pytest.raises(ValueError):
        renderer.render_pointer(
            dict_to_render=placholder_transform_question_json,
            pointer_to_render="/title",
            list_item_id=None,
            placeholder_parser=PlaceholderParser(
                language="en",
                answer_store=AnswerStore(),
                list_store=ListStore(),
                metadata=None,
                response_metadata={},
                schema=mock_schema,
                location=None,
                renderer=renderer,
                progress_store=ProgressStore(),
            ),
        )


def test_errors_on_invalid_json(mock_schema):
    renderer = get_placeholder_render()
    with pytest.raises(ValueError):
        dict_to_render = {"invalid": {"no": "placeholders", "in": "this"}}
        renderer.render_pointer(
            dict_to_render=dict_to_render,
            pointer_to_render="/invalid",
            list_item_id=None,
            placeholder_parser=PlaceholderParser(
                language="en",
                answer_store=AnswerStore(),
                list_store=ListStore(),
                metadata=None,
                response_metadata={},
                schema=mock_schema,
                location=None,
                renderer=renderer,
                progress_store=ProgressStore(),
            ),
        )


def test_renders_text_plural_from_answers():
    answer_store = AnswerStore([{"answer_id": "number-of-people", "value": 1}])

    renderer = get_placeholder_render(answer_store=answer_store)
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


def test_renders_text_plural_from_list():
    renderer = get_placeholder_render()

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


def test_renders_text_plural_from_metadata():
    metadata = {"some_value": 100}
    renderer = get_placeholder_render(metadata=metadata)

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


def test_renders_json_dynamic_answers(
    placeholder_transform_question_dynamic_answers_json,
):
    json_to_render = placeholder_transform_question_dynamic_answers_json

    answer_store = AnswerStore(
        [
            {"answer_id": "any-supermarket-answer", "value": "Yes"},
            {
                "answer_id": "supermarket-name",
                "value": "Tesco",
                "list_item_id": "yWKpNY",
            },
            {
                "answer_id": "supermarket-name",
                "value": "Aldi",
                "list_item_id": "vtbSnC",
            },
            {"answer_id": "list-collector-answer", "value": "No"},
        ]
    )

    list_store = ListStore([{"items": ["yWKpNY", "vtbSnC"], "name": "supermarkets"}])

    renderer = get_placeholder_render_dynamic_answers(
        answer_store=answer_store, list_store=list_store
    )
    rendered_schema = renderer.render(data_to_render=json_to_render, list_item_id=None)
    rendered_label_first = rendered_schema["answers"][0]["label"]
    rendered_id_first = rendered_schema["answers"][0]["id"]
    rendered_label_second = rendered_schema["answers"][1]["label"]
    rendered_id_second = rendered_schema["answers"][1]["id"]

    assert rendered_label_first == "Percentage of shopping at Tesco"
    assert rendered_id_first == "percentage-of-shopping-yWKpNY"
    assert rendered_label_second == "Percentage of shopping at Aldi"
    assert rendered_id_second == "percentage-of-shopping-vtbSnC"


def test_renders_json_dynamic_answers_pointer(
    placeholder_transform_question_dynamic_answers_pointer_json,
):
    json_to_render = placeholder_transform_question_dynamic_answers_pointer_json

    answer_store = AnswerStore(
        [
            {"answer_id": "any-supermarket-answer", "value": "Yes"},
            {
                "answer_id": "supermarket-name",
                "value": "Tesco",
                "list_item_id": "yWKpNY",
            },
            {
                "answer_id": "supermarket-name",
                "value": "Aldi",
                "list_item_id": "vtbSnC",
            },
            {"answer_id": "list-collector-answer", "value": "No"},
        ]
    )

    list_store = ListStore([{"items": ["yWKpNY", "vtbSnC"], "name": "supermarkets"}])

    renderer = get_placeholder_render_dynamic_answers(
        answer_store=answer_store, list_store=list_store
    )
    rendered_schema = renderer.render(data_to_render=json_to_render, list_item_id=None)
    rendered_label_first = rendered_schema["question"]["answers"][0]["label"]
    rendered_id_first = rendered_schema["question"]["answers"][0]["id"]
    rendered_label_second = rendered_schema["question"]["answers"][1]["label"]
    rendered_id_second = rendered_schema["question"]["answers"][1]["id"]

    assert rendered_label_first == "Percentage of shopping at Tesco"
    assert rendered_id_first == "percentage-of-shopping-yWKpNY"
    assert rendered_label_second == "Percentage of shopping at Aldi"
    assert rendered_id_second == "percentage-of-shopping-vtbSnC"


def get_placeholder_render_dynamic_answers(
    *,
    language="en",
    answer_store=AnswerStore(),
    list_store=ListStore(),
    progress_store=ProgressStore(),
    metadata=None,
    response_metadata=None,
):
    schema = load_schema_from_name("test_dynamic_answers_list_source")
    return PlaceholderRenderer(
        language=language,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        metadata=metadata or {},
        response_metadata=response_metadata or {},
        schema=schema,
    )


def get_placeholder_render(
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
        schema=MagicMock(),
        progress_store=ProgressStore(),
        location=Location(section_id="default-section"),
    )
    return renderer
