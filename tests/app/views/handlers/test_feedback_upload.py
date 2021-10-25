import uuid
from datetime import datetime, timezone

import pytest
from freezegun import freeze_time

from app.data_models.session_data import SessionData
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.handlers.feedback import FeedbackMetadata, FeedbackPayload

tx_id = str(uuid.uuid4())
response_id = "1234567890123456"
period_str = "2016-01-01"
period_id = "2016-02-01"
ref_p_start_date = "2016-02-02"
ref_p_end_date = "2016-03-03"
ru_ref = "432423423423"
ru_name = "ru_name"
user_id = "789473423"
schema_name = "1_0000"
feedback_count = 1
display_address = "68 Abingdon Road, Goathill"
form_type = "I"
collection_exercise_sid = "test-sid"
case_id = "case_id"
survey_id = "021"
data_version = "0.0.1"
feedback_type = "Feedback type"
feedback_text = "Feedback text"
feedback_type_question_category = "Feedback type question category"
started_at = str(datetime.now(tz=timezone.utc).isoformat())
language_code = "cy"
case_type = "I"
channel = "H"
case_ref = "1000000000000001"
region_code = "GB_WLS"


@pytest.fixture()
def session_data():
    return SessionData(
        tx_id=tx_id,
        schema_name=schema_name,
        response_id=response_id,
        period_str=period_str,
        language_code=language_code,
        launch_language_code=None,
        survey_url=None,
        ru_name=ru_name,
        ru_ref=ru_ref,
        case_id=case_id,
        feedback_count=feedback_count,
    )


@pytest.fixture()
def schema():
    return QuestionnaireSchema({"survey_id": survey_id, "data_version": data_version})


@pytest.fixture()
def metadata():
    return {
        "tx_id": tx_id,
        "user_id": user_id,
        "schema_name": schema_name,
        "collection_exercise_sid": collection_exercise_sid,
        "period_id": period_id,
        "period_str": period_str,
        "ref_p_start_date": ref_p_start_date,
        "ref_p_end_date": ref_p_end_date,
        "ru_ref": ru_ref,
        "response_id": response_id,
        "form_type": form_type,
        "display_address": display_address,
        "case_type": case_type,
        "channel": channel,
        "case_ref": case_ref,
        "region_code": region_code,
    }


@pytest.fixture()
def response_metadata():
    return {
        "started_at": started_at,
    }


@freeze_time(datetime.now(tz=timezone.utc).isoformat())
def test_feedback_payload(session_data, schema, metadata, response_metadata):
    feedback_payload = FeedbackPayload(
        metadata=metadata,
        response_metadata=response_metadata,
        schema=schema,
        case_id=case_id,
        submission_language_code=language_code,
        feedback_count=session_data.feedback_count,
        feedback_text=feedback_text,
        feedback_type=feedback_type,
    )

    expected_payload = {
        "collection": {
            "exercise_sid": collection_exercise_sid,
            "period": period_id,
            "schema_name": schema_name,
        },
        "data": {
            "feedback_count": str(feedback_count),
            "feedback_text": feedback_text,
            "feedback_type": feedback_type,
        },
        "form_type": form_type,
        "launch_language_code": "en",
        "metadata": {
            "display_address": display_address,
            "ref_period_end_date": ref_p_end_date,
            "ref_period_start_date": ref_p_start_date,
            "ru_ref": ru_ref,
            "user_id": user_id,
        },
        "origin": "uk.gov.ons.edc.eq",
        "case_id": case_id,
        "started_at": started_at,
        "submitted_at": datetime.now(tz=timezone.utc).isoformat(),
        "flushed": False,
        "survey_id": survey_id,
        "submission_language_code": language_code,
        "tx_id": tx_id,
        "type": "uk.gov.ons.edc.eq:feedback",
        "version": data_version,
        "case_type": case_type,
        "channel": channel,
        "region_code": region_code,
        "case_ref": case_ref,
    }

    assert expected_payload == feedback_payload()


def test_feedback_metadata():
    feedback_metadata = FeedbackMetadata(case_id, tx_id)

    expected_metadata = {
        "case_id": case_id,
        "tx_id": tx_id,
    }

    assert feedback_metadata() == expected_metadata
