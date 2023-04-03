from datetime import datetime, timezone

import pytest
from freezegun import freeze_time

from app.data_models import AnswerStore, QuestionnaireStore, ListStore
from app.questionnaire import Location, QuestionnaireSchema
from app.views.handlers.question import Question

from .conftest import set_storage_data


@pytest.mark.usefixtures("app")
@freeze_time("2022-06-01T15:34:54+00:00")
def test_question_with_dynamic_answers(storage, language, mocker):
    submitted_at = datetime.now(timezone.utc)
    set_storage_data(storage, submitted_at=submitted_at)

    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.answer_store = AnswerStore(
        [
            {
                "answer_id": "supermarket-name",
                "value": "Tesco",
                "list_item_id": "tUJzGV",
            },
            {
                "answer_id": "supermarket-name",
                "value": "Aldi",
                "list_item_id": "vhECeh",
            },
        ]
    )
    questionnaire_store.list_store = ListStore(
        [{"items": ["tUJzGV", "vhECeh"], "name": "supermarkets"}]
    )
    schema = QuestionnaireSchema(
        {
            "sections": [
                {
                    "id": "section",
                    "groups": [
                        {
                            "blocks": [
                                {
                                    "id": "list-collector",
                                    "type": "ListCollector",
                                    "for_list": "supermarkets",
                                    "question": {
                                        "id": "confirmation-question",
                                        "type": "General",
                                        "title": "Do you need to add any more supermarkets?",
                                        "answers": [
                                            {
                                                "id": "list-collector-answer",
                                                "mandatory": True,
                                                "type": "Radio",
                                                "options": [
                                                    {
                                                        "label": "Yes",
                                                        "value": "Yes",
                                                        "action": {
                                                            "type": "RedirectToListAddBlock"
                                                        },
                                                    },
                                                    {"label": "No", "value": "No"},
                                                ],
                                            }
                                        ],
                                    },
                                    "add_block": {
                                        "id": "add-supermarket",
                                        "type": "ListAddQuestion",
                                        "cancel_text": "Don’t need to add any other supermarkets?",
                                        "question": {
                                            "guidance": {
                                                "contents": [
                                                    {
                                                        "description": "If you need to add multiple supermarkets, you can do this on the next page."
                                                    }
                                                ]
                                            },
                                            "id": "add-question",
                                            "type": "General",
                                            "title": "Which supermarkets do you use for your weekly shopping?",
                                            "answers": [
                                                {
                                                    "id": "supermarket-name",
                                                    "label": "Supermarket",
                                                    "mandatory": True,
                                                    "type": "TextField",
                                                }
                                            ],
                                        },
                                    },
                                    "edit_block": {
                                        "id": "edit-supermarket",
                                        "type": "ListEditQuestion",
                                        "cancel_text": "Don’t need to change anything?",
                                        "question": {
                                            "id": "edit-question",
                                            "type": "General",
                                            "title": "What is the name of the supermarket?",
                                            "answers": [
                                                {
                                                    "id": "supermarket-name",
                                                    "label": "Supermarket",
                                                    "mandatory": True,
                                                    "type": "TextField",
                                                }
                                            ],
                                        },
                                    },
                                    "remove_block": {
                                        "id": "remove-supermarket",
                                        "type": "ListRemoveQuestion",
                                        "cancel_text": "Don’t need to remove this supermarket?",
                                        "question": {
                                            "id": "remove-question",
                                            "type": "General",
                                            "title": "Are you sure you want to remove this supermarket?",
                                            "warning": "All of the information about this supermarket will be deleted",
                                            "answers": [
                                                {
                                                    "id": "remove-confirmation",
                                                    "mandatory": True,
                                                    "type": "Radio",
                                                    "options": [
                                                        {
                                                            "label": "Yes",
                                                            "value": "Yes",
                                                            "action": {
                                                                "type": "RemoveListItemAndAnswers"
                                                            },
                                                        },
                                                        {"label": "No", "value": "No"},
                                                    ],
                                                }
                                            ],
                                        },
                                    },
                                    "summary": {
                                        "title": "Supermarkets",
                                        "item_title": {
                                            "text": "{supermarket_name}",
                                            "placeholders": [
                                                {
                                                    "placeholder": "supermarket_name",
                                                    "transforms": [
                                                        {
                                                            "arguments": {
                                                                "delimiter": " ",
                                                                "list_to_concatenate": [
                                                                    {
                                                                        "source": "answers",
                                                                        "identifier": "supermarket-name",
                                                                    }
                                                                ],
                                                            },
                                                            "transform": "concatenate_list",
                                                        }
                                                    ],
                                                }
                                            ],
                                        },
                                    },
                                },
                                {
                                    "type": "Question",
                                    "id": "dynamic-answer",
                                    "question": {
                                        "dynamic_answers": {
                                            "values": {
                                                "source": "list",
                                                "identifier": "supermarkets",
                                            },
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
                                        "answers": [],
                                        "id": "dynamic-answer-question",
                                        "title": "What percent of your shopping do you do at each of the following supermarket?",
                                        "type": "General",
                                    },
                                },
                            ],
                            "id": "group",
                        }
                    ],
                }
            ]
        }
    )
    mocker.patch(
        "app.views.handlers.question.Question.is_location_valid",
        return_value=True,
    )
    question = Question(
        current_location=Location(section_id="section", block_id="dynamic-answer"),
        form_data=None,
        language=language,
        questionnaire_store=questionnaire_store,
        request_args=mocker.MagicMock(),
        schema=schema,
    )

    form = question.form
    assert form.question["answers"] == [
        {
            "decimal_places": 0,
            "id": "percentage-of-shopping-tUJzGV",
            "label": "Percentage of shopping at Tesco",
            "mandatory": False,
            "maximum": {"value": 100},
            "type": "Percentage",
        },
        {
            "decimal_places": 0,
            "id": "percentage-of-shopping-vhECeh",
            "label": "Percentage of shopping at Aldi",
            "mandatory": False,
            "maximum": {"value": 100},
            "type": "Percentage",
        },
    ]
