from datetime import datetime, timezone

from freezegun import freeze_time

from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.views.handlers.feedback import FeedbackMetadata, FeedbackPayload

from .conftest import (
    case_id,
    case_ref,
    case_type,
    channel,
    collection_exercise_sid,
    data_version,
    display_address,
    feedback_count,
    feedback_text,
    feedback_type,
    form_type,
    language_code,
    period_id,
    ref_p_end_date,
    ref_p_start_date,
    region_code,
    ru_ref,
    schema_name,
    started_at,
    survey_id,
    tx_id,
    user_id,
)


@freeze_time(datetime.now(tz=timezone.utc).isoformat())
def test_feedback_payload(
    session_data_feedback, schema_feedback, metadata, response_metadata
):
    feedback_payload = FeedbackPayload(
        metadata=metadata,
        response_metadata=response_metadata,
        schema=schema_feedback,
        case_id=case_id,
        submission_language_code=language_code,
        feedback_count=session_data_feedback.feedback_count,
        feedback_text=feedback_text,
        feedback_type=feedback_type,
    )

    expected_payload = {
        "collection": {
            "exercise_sid": collection_exercise_sid,
            "instrument_id": "I",
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


def test_submission_language_code_uses_default_language_when_session_language_none(
    session_data_feedback, schema_feedback, metadata, response_metadata
):
    feedback_payload = FeedbackPayload(
        metadata=metadata,
        response_metadata=response_metadata,
        schema=schema_feedback,
        case_id=case_id,
        submission_language_code=None,
        feedback_count=session_data_feedback.feedback_count,
        feedback_text=feedback_text,
        feedback_type=feedback_type,
    )

    assert feedback_payload()["submission_language_code"] == DEFAULT_LANGUAGE_CODE


def test_feedback_metadata():
    feedback_metadata = FeedbackMetadata(case_id, tx_id)

    expected_metadata = {
        "case_id": case_id,
        "tx_id": tx_id,
    }

    assert feedback_metadata() == expected_metadata
