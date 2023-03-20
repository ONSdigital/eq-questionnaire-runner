from datetime import datetime, timezone

import pytest
from freezegun import freeze_time

from app.data_models import AnswerStore, QuestionnaireStore
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
            {"answer_id": "mandatory-checkbox-answer", "value": ["Tesco", "Aldi"]},
        ]
    )
    schema = QuestionnaireSchema(
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
                                                    {"label": "Aldi", "value": "Aldi"},
                                                    {"label": "Asda", "value": "Asda"},
                                                    {
                                                        "label": "Sainsbury’s",
                                                        "value": "Sainsbury’s",
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
    )
    mocker.patch(
        "app.views.handlers.question.Question.is_location_valid",
        return_value=True,
    )
    question = Question(
        current_location=Location(
            section_id="default-section", block_id="non-mandatory-checkbox"
        ),
        form_data=None,
        language=language,
        questionnaire_store=questionnaire_store,
        request_args=mocker.MagicMock(),
        schema=schema,
    )

    form = question.form
    assert form.question["answers"] == [
        {
            "label": "Percentage of shopping at Tesco",
            "id": "percentage-of-shopping-tesco",
            "mandatory": False,
            "type": "Percentage",
            "maximum": {"value": 100},
            "decimal_places": 0,
        },
        {
            "label": "Percentage of shopping at Aldi",
            "id": "percentage-of-shopping-aldi",
            "mandatory": False,
            "type": "Percentage",
            "maximum": {"value": 100},
            "decimal_places": 0,
        },
    ]
