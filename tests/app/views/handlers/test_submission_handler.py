from datetime import datetime, timedelta
from unittest.mock import Mock

from dateutil.tz import tzutc
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
            questionnaire_id="questionnaire_id",
        )
        self.session_store = SessionStore("user_ik", "pepper", "eq_session_id")
        self.expires_at = datetime.now(tzutc()) + timedelta(seconds=5)

    def test_submission_language_code_in_payload(self):
        session_store = self.session_store.create(
            "eq_session_id", "user_id", self.session_data, self.expires_at
        )
        storage = Mock()
        storage.get_user_data = Mock(return_value=("{}", 1))

        with patch(
            "app.views.handlers.submission.get_session_store",
            return_value=session_store,
        ):
            with patch(
                "app.views.handlers.submission.convert_answers", return_value={}
            ):
                submission_handler = SubmissionHandler(
                    QuestionnaireSchema({}), QuestionnaireStore(storage), {}
                )
                assert (
                    submission_handler.get_payload()["submission_language_code"] == "cy"
                )
