from datetime import datetime, timezone
import pytest

from freezegun import freeze_time

from app.data_models.session_store import SessionStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
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
