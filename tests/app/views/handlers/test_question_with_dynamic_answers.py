from datetime import datetime, timezone

import pytest
from freezegun import freeze_time

from app.data_models import AnswerStore, ListStore, QuestionnaireStore
from app.questionnaire import Location
from app.utilities.schema import load_schema_from_name
from app.views.handlers.question import Question
from tests.app.parser.conftest import get_response_expires_at
from tests.app.views.handlers.conftest import set_storage_data


@pytest.mark.usefixtures("app")
@freeze_time("2022-06-01T15:34:54+00:00")
def test_question_with_dynamic_answers(storage, language, mocker):
    submitted_at = datetime.now(timezone.utc)
    set_storage_data(storage, submitted_at=submitted_at)

    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.stores.answer_store = AnswerStore(
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
    questionnaire_store.stores.list_store = ListStore(
        [{"items": ["tUJzGV", "vhECeh"], "name": "supermarkets"}]
    )
    questionnaire_store.set_metadata({"response_expires_at": get_response_expires_at()})
    schema = load_schema_from_name("test_dynamic_answers_list_source")

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
    question.handle_post()

    assert form.question["answers"] == [
        {
            "decimal_places": 0,
            "id": "percentage-of-shopping-tUJzGV",
            "label": "Percentage of shopping at Tesco",
            "list_item_id": "tUJzGV",
            "mandatory": False,
            "maximum": {"value": 100},
            "original_answer_id": "percentage-of-shopping",
            "type": "Percentage",
        },
        {
            "decimal_places": 0,
            "id": "percentage-of-shopping-vhECeh",
            "label": "Percentage of shopping at Aldi",
            "list_item_id": "vhECeh",
            "mandatory": False,
            "maximum": {"value": 100},
            "original_answer_id": "percentage-of-shopping",
            "type": "Percentage",
        },
        {
            "decimal_places": 0,
            "id": "days-a-week-tUJzGV",
            "label": "How many days a week you shop at Tesco",
            "list_item_id": "tUJzGV",
            "mandatory": False,
            "maximum": {"value": 7},
            "minimum": {"value": 1},
            "original_answer_id": "days-a-week",
            "type": "Number",
        },
        {
            "decimal_places": 0,
            "id": "days-a-week-vhECeh",
            "label": "How many days a week you shop at Aldi",
            "list_item_id": "vhECeh",
            "mandatory": False,
            "maximum": {"value": 7},
            "minimum": {"value": 1},
            "original_answer_id": "days-a-week",
            "type": "Number",
        },
        {
            "id": "based-checkbox-answer",
            "instruction": "Select any answers that apply",
            "label": "Are supermarkets UK or non UK based?",
            "mandatory": False,
            "options": [
                {"label": "UK based supermarkets", "value": "UK based supermarkets"},
                {
                    "label": "Non UK based supermarkets",
                    "value": "Non UK based supermarkets",
                },
            ],
            "type": "Checkbox",
        },
    ]
