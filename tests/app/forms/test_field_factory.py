import pytest

from app.data_models import ProgressStore, SupplementaryDataStore
from app.forms import error_messages
from app.forms.field_handlers import get_field_handler
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import ValueSourceResolver


def test_invalid_field_type_raises_on_invalid(answer_store, list_store):
    schema = QuestionnaireSchema(
        {
            "questionnaire_flow": {
                "type": "Linear",
                "options": {"summary": {"collapsible": False}},
            }
        }
    )

    metadata = {
        "user_id": "789473423",
        "schema_name": "0000",
        "collection_exercise_sid": "test-sid",
        "period_id": "2016-02-01",
        "period_str": "2016-01-01",
        "ref_p_start_date": "2016-02-02",
        "ref_p_end_date": "2016-03-03",
        "ru_ref": "432423423423",
        "ru_name": "Apple",
        "return_by": "2016-07-07",
        "case_id": "1234567890",
        "case_ref": "1000000000000001",
    }

    response_metadata = {}

    value_source_resolver = ValueSourceResolver(
        answer_store=answer_store,
        list_store=list_store,
        metadata=metadata,
        response_metadata=response_metadata,
        schema=schema,
        location=None,
        list_item_id=None,
        escape_answer_values=False,
        progress_store=ProgressStore(),
        supplementary_data_store=SupplementaryDataStore(),
    )

    rule_evaluator = RuleEvaluator(
        answer_store=answer_store,
        list_store=list_store,
        metadata=metadata,
        response_metadata=response_metadata,
        schema=schema,
        location=None,
        progress_store=ProgressStore(),
        supplementary_data_store=SupplementaryDataStore(),
    )

    # Given
    invalid_field_type = "Football"
    # When / Then
    with pytest.raises(KeyError):
        get_field_handler(
            answer_schema={"type": invalid_field_type},
            value_source_resolver=value_source_resolver,
            rule_evaluator=rule_evaluator,
            error_messages=error_messages,
        )
