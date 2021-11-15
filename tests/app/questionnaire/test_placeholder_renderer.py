from unittest.mock import Mock, patch

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.questionnaire.placeholder_renderer import (
    PlaceholderRenderer,
    find_pointers_containing,
)
from tests.app.app_context_test_case import AppContextTestCase


@patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
class TestPlaceholderRenderer(AppContextTestCase):
    def setUp(self):
        super().setUp()

        self.question_json = {
            "id": "confirm-date-of-birth-proxy",
            "title": "Confirm date of birth",
            "type": "General",
            "answers": [
                {
                    "id": "confirm-date-of-birth-answer-proxy",
                    "mandatory": True,
                    "options": [
                        {
                            "label": {
                                "text": "{person_name_possessive} age is {age}. Is this correct?",
                                "placeholders": [
                                    {
                                        "placeholder": "person_name_possessive",
                                        "transforms": [
                                            {
                                                "arguments": {
                                                    "delimiter": " ",
                                                    "list_to_concatenate": [
                                                        {
                                                            "source": "answers",
                                                            "identifier": "first-name",
                                                        },
                                                        {
                                                            "source": "answers",
                                                            "identifier": "last-name",
                                                        },
                                                    ],
                                                },
                                                "transform": "concatenate_list",
                                            },
                                            {
                                                "arguments": {
                                                    "string_to_format": {
                                                        "source": "previous_transform"
                                                    }
                                                },
                                                "transform": "format_possessive",
                                            },
                                        ],
                                    },
                                    {
                                        "placeholder": "age",
                                        "transforms": [
                                            {
                                                "transform": "calculate_date_difference",
                                                "arguments": {
                                                    "first_date": {
                                                        "source": "answers",
                                                        "identifier": "date-of-birth-answer",
                                                    },
                                                    "second_date": {"value": "now"},
                                                },
                                            }
                                        ],
                                    },
                                ],
                            },
                            "value": "Yes",
                        },
                        {
                            "label": "No, I need to change their date of birth",
                            "value": "No",
                        },
                    ],
                    "type": "Radio",
                }
            ],
        }

        self.pointers = list(
            find_pointers_containing(self.question_json, "placeholders")
        )

    def test_correct_pointers(self):
        assert self.pointers[0] == "/answers/0/options/0/label"

    def test_renders_pointer(self):
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

        json_to_render = self.question_json.copy()
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
            self.question_json, "/answers/0/options/0/label", list_item_id=None
        )

        assert rendered == "Hal Abelson’s age is 28 years. Is this correct?"

    def test_renders_json(self):
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
        json_to_render = self.question_json.copy()
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
        rendered_schema = renderer.render(json_to_render, list_item_id=None)
        rendered_label = rendered_schema["answers"][0]["options"][0]["label"]

        assert rendered_label == "Alfred Aho’s age is 33 years. Is this correct?"

    def test_renders_json_uses_language(self):
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
        json_to_render = self.question_json.copy()
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
        rendered_schema = renderer.render(json_to_render, list_item_id=None)
        rendered_label = rendered_schema["answers"][0]["options"][0]["label"]

        assert rendered_label == "Alfred Aho age is 33 years. Is this correct?"

    def test_errors_on_invalid_pointer(self):
        renderer = get_placeholder_render()

        with self.assertRaises(ValueError):
            renderer.render_pointer(self.question_json, "/title", list_item_id=None)

    def test_errors_on_invalid_json(self):
        renderer = get_placeholder_render()
        with self.assertRaises(ValueError):
            dict_to_render = {"invalid": {"no": "placeholders", "in": "this"}}
            renderer.render_pointer(dict_to_render, "/invalid", list_item_id=None)


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


def get_placeholder_render(
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
        schema=Mock(),
    )
    return renderer
