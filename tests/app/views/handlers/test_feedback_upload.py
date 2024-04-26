from datetime import datetime, timezone

from freezegun import freeze_time

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.views.handlers.feedback import FeedbackMetadata, FeedbackPayloadV2
from tests.app.views.handlers.conftest import (
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
    period_str,
    ref_p_end_date,
    ref_p_start_date,
    region_code,
    ru_name,
    ru_ref,
    schema_name,
    started_at,
    survey_id,
    tx_id,
    user_id,
)


@freeze_time(datetime.now(tz=timezone.utc).isoformat())
def test_feedback_payload_v2(
    session_data_feedback, schema_feedback, metadata_v2, response_metadata
):
    feedback_payload = FeedbackPayloadV2(
        metadata=metadata_v2,
        response_metadata=response_metadata,
        schema=schema_feedback,
        case_id=case_id,
        submission_language_code=language_code,
        feedback_count=session_data_feedback.feedback_count,
        feedback_text=feedback_text,
        feedback_type=feedback_type,
    )

    expected_payload = {
        "case_id": case_id,
        "channel": channel,
        "collection_exercise_sid": collection_exercise_sid,
        "data": {
            "feedback_count": str(feedback_count),
            "feedback_text": feedback_text,
            "feedback_type": feedback_type,
        },
        "data_version": data_version,
        "flushed": False,
        "launch_language_code": "en",
        "origin": "uk.gov.ons.edc.eq",
        "region_code": region_code,
        "schema_name": schema_name,
        "started_at": started_at,
        "submission_language_code": language_code,
        "submitted_at": datetime.now(tz=timezone.utc).isoformat(),
        "survey_metadata": {
            "survey_id": survey_id,
            "case_ref": case_ref,
            "case_type": case_type,
            "display_address": display_address,
            "form_type": form_type,
            "period_id": period_id,
            "period_str": period_str,
            "ref_p_end_date": ref_p_end_date,
            "ref_p_start_date": ref_p_start_date,
            "ru_name": ru_name,
            "ru_ref": ru_ref,
            "user_id": user_id,
        },
        "tx_id": tx_id,
        "type": "uk.gov.ons.edc.eq:feedback",
        "version": AuthPayloadVersion.V2.value,
    }

    assert expected_payload == feedback_payload()


def test_submission_language_code_uses_default_language_when_session_language_none(
    session_data_feedback, schema_feedback, metadata, response_metadata
):
    feedback_payload = FeedbackPayloadV2(
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


def test_feedback_metadata_with_receipting_keys():
    receipting_keys = {"qid": "1"}

    feedback_metadata = FeedbackMetadata(case_id, tx_id, **receipting_keys)

    expected_metadata = {"case_id": case_id, "tx_id": tx_id, "qid": "1"}

    assert feedback_metadata() == expected_metadata
