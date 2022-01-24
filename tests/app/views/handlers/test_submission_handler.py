from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

from freezegun import freeze_time
from mock import patch

from app.data_models import QuestionnaireStore
from app.data_models.session_data import SessionData
from app.data_models.session_store import SessionStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.handlers.submission import SubmissionHandler
from tests.app.app_context_test_case import AppContextTestCase


class TestSubmissionPayload(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.session_data = SessionData(
            tx_id="tx_id",
            schema_name="schema_name",
            response_id="response_id",
            period_str="period_str",
            language_code="cy",
            launch_language_code="en",
            survey_url=None,
            ru_name="ru_name",
            ru_ref="ru_ref",
            case_id="0123456789000000",
        )
        self.expires_at = datetime.now(timezone.utc) + timedelta(seconds=5)
        self.session_store = SessionStore("user_ik", "pepper", "eq_session_id").create(
            "eq_session_id", "user_id", self.session_data, self.expires_at
        )

    @patch("app.views.handlers.submission.convert_answers", Mock(return_value={}))
    def test_submission_language_code_uses_session_data_language_if_present(self):
        with patch(
            "app.views.handlers.submission.get_session_store",
            return_value=self.session_store,
        ):
            submission_handler = SubmissionHandler(
                QuestionnaireSchema({}), self.questionnaire_store_mock(), {}
            )
            assert submission_handler.get_payload()["submission_language_code"] == "cy"

    @patch("app.views.handlers.submission.convert_answers", Mock(return_value={}))
    def test_submission_language_code_uses_default_language_if_session_data_language_not_present(
        self,
    ):
        self.session_data.language_code = None
        self.session_data.launch_language_code = None
        session_store = SessionStore("user_ik", "pepper", "eq_session_id").create(
            "eq_session_id", "user_id", self.session_data, self.expires_at
        )

        with patch(
            "app.views.handlers.submission.get_session_store",
            return_value=session_store,
        ):
            submission_handler = SubmissionHandler(
                QuestionnaireSchema({}), self.questionnaire_store_mock(), {}
            )
            assert submission_handler.get_payload()["submission_language_code"] == "en"

    @patch(
        "app.views.handlers.submission.SubmissionHandler.get_payload",
        Mock(return_value={}),
    )
    @freeze_time(datetime.now(timezone.utc).replace(second=0, microsecond=0))
    @patch(
        "app.views.handlers.submission.SubmissionHandler.get_payload",
        Mock(return_value={}),
    )
    def test_submit_view_submitted_response_true_submitted_at_set(self):
        questionnaire_store = self.questionnaire_store_mock()
        questionnaire_store.delete = Mock()
        questionnaire_store.save = Mock()

        with self.app_request_context():
            with patch(
                "app.views.handlers.submission.get_session_store",
                return_value=self.session_store,
            ):
                submission_handler = SubmissionHandler(
                    QuestionnaireSchema(
                        {"submission": {"view_submitted_response": "True"}}
                    ),
                    questionnaire_store,
                    full_routing_path=[],
                )
                submission_handler.submit_questionnaire()

                assert questionnaire_store.submitted_at == datetime.now(timezone.utc)
                assert questionnaire_store.save.called
                assert not questionnaire_store.delete.called

    @staticmethod
    def questionnaire_store_mock():
        storage = Mock()
        storage.get_user_data = Mock(return_value=("{}", "ce_id", 1, None))
        questionnaire_store = QuestionnaireStore(storage)
        questionnaire_store.metadata = {"tx_id": "tx_id", "case_id": "case_id"}
        return questionnaire_store
