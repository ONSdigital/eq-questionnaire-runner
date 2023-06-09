from datetime import datetime, timezone

import pytest
from freezegun import freeze_time

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.data_models.session_store import SessionStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.schema import load_schema_from_name
from app.views.handlers.submission import SubmissionHandler


@pytest.mark.usefixtures("app")
def test_submission_language_code_uses_session_data_language_if_present(
    submission_payload_session_store, mock_questionnaire_store, mocker
):
    mocker.patch(
        "app.views.handlers.submission.get_session_store",
        return_value=submission_payload_session_store,
    )
    mocker.patch(
        "app.views.handlers.submission.convert_answers", mocker.Mock(return_value={})
    )
    submission_handler = SubmissionHandler(
        QuestionnaireSchema({}), mock_questionnaire_store, {}
    )
    assert submission_handler.get_payload()["submission_language_code"] == "cy"


@pytest.mark.usefixtures("app")
def test_submission_language_code_uses_default_language_if_session_data_language_none(
    submission_payload_session_data,
    submission_payload_expires_at,
    mock_questionnaire_store,
    mocker,
):
    mocker.patch(
        "app.views.handlers.submission.convert_answers", mocker.Mock(return_value={})
    )
    submission_payload_session_data.language_code = None
    submission_payload_session_data.launch_language_code = None
    session_store = SessionStore("user_ik", "pepper", "eq_session_id").create(
        "eq_session_id",
        "user_id",
        submission_payload_session_data,
        submission_payload_expires_at,
    )

    mocker.patch(
        "app.views.handlers.submission.get_session_store",
        return_value=session_store,
    )
    submission_handler = SubmissionHandler(
        QuestionnaireSchema({}), mock_questionnaire_store, {}
    )
    assert submission_handler.get_payload()["submission_language_code"] == "en"


@freeze_time(datetime.now(timezone.utc).replace(second=0, microsecond=0))
def test_submit_view_submitted_response_true_submitted_at_set(
    app, submission_payload_session_store, mock_questionnaire_store, mocker
):
    mocker.patch(
        "app.views.handlers.submission.SubmissionHandler.get_payload",
        mocker.Mock(return_value={}),
    )
    mock_questionnaire_store.delete = mocker.Mock()
    mock_questionnaire_store.save = mocker.Mock()

    with app.test_request_context():
        mocker.patch(
            "app.views.handlers.submission.get_session_store",
            return_value=submission_payload_session_store,
        )
        submission_handler = SubmissionHandler(
            QuestionnaireSchema({"submission": {"view_submitted_response": "True"}}),
            mock_questionnaire_store,
            full_routing_path=[],
        )
        submission_handler.submit_questionnaire()

        assert mock_questionnaire_store.submitted_at == datetime.now(timezone.utc)
        assert mock_questionnaire_store.save.called
        assert not mock_questionnaire_store.delete.called


@freeze_time(datetime.now(timezone.utc).replace(second=0, microsecond=0))
@pytest.mark.usefixtures("app")
def test_submission_payload_structure_v1(
    app, submission_payload_session_store, mock_questionnaire_store, mocker
):
    expected_payload = {
        "case_id": "case_id",
        "collection": {
            "exercise_sid": "ce_sid",
            "period": "2016-02-01",
            "schema_name": "1_0000",
        },
        "data": {"answers": [], "lists": []},
        "flushed": False,
        "launch_language_code": "en",
        "metadata": {"ru_ref": "432423423423", "user_id": "789473423"},
        "origin": "uk.gov.ons.edc.eq",
        "submission_language_code": "cy",
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "survey_id": "0",
        "tx_id": "tx_id",
        "type": "uk.gov.ons.edc.eq:surveyresponse",
        "version": "0.0.3",
    }

    with app.test_request_context():
        mocker.patch(
            "app.views.handlers.submission.get_session_store",
            return_value=submission_payload_session_store,
        )
        schema = load_schema_from_name("test_checkbox")

        submission_handler = SubmissionHandler(
            schema,
            mock_questionnaire_store,
            full_routing_path=[],
        )
        payload = submission_handler.get_payload()

        assert expected_payload == payload


@freeze_time(datetime.now(timezone.utc).replace(second=0, microsecond=0))
@pytest.mark.usefixtures("app")
def test_submission_payload_structure_v2(
    app, submission_payload_session_store, mock_questionnaire_store_v2, mocker
):
    expected_payload = {
        "case_id": "case_id",
        "tx_id": "tx_id",
        "type": "uk.gov.ons.edc.eq:surveyresponse",
        "version": AuthPayloadVersion.V2.value,
        "data_version": "0.0.3",
        "origin": "uk.gov.ons.edc.eq",
        "collection_exercise_sid": "ce_sid",
        "schema_name": "1_0000",
        "flushed": False,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "launch_language_code": "en",
        "channel": "H",
        "region_code": "GB_WLS",
        "survey_metadata": {
            "period_id": "2016-02-01",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "432423423423",
            "ru_name": "ru_name",
            "case_type": "I",
            "form_type": "I",
            "case_ref": "1000000000000001",
            "display_address": "68 Abingdon Road, Goathill",
            "user_id": "789473423",
            "survey_id": "0",
        },
        "submission_language_code": "cy",
        "data": {"answers": [], "lists": []},
    }

    with app.test_request_context():
        mocker.patch(
            "app.views.handlers.submission.get_session_store",
            return_value=submission_payload_session_store,
        )
        schema = load_schema_from_name("test_checkbox")

        submission_handler = SubmissionHandler(
            schema,
            mock_questionnaire_store_v2,
            full_routing_path=[],
        )
        payload = submission_handler.get_payload()

        assert expected_payload == payload
