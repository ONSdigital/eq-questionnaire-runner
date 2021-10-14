import uuid
from datetime import datetime, timedelta, timezone

from app.data_models.session_data import SessionData
from app.data_models.session_store import SessionStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.handlers.feedback import FeedbackMetadata, FeedbackPayload
from tests.app.app_context_test_case import AppContextTestCase


class TestFeedbackUpload(AppContextTestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        super().setUp()

        self.tx_id = str(uuid.uuid4())
        self.response_id = "1234567890123456"
        self.period_str = "2016-01-01"
        self.period_id = "2016-02-01"
        self.ref_p_start_date = "2016-02-02"
        self.ref_p_end_date = "2016-03-03"
        self.ru_ref = "432423423423"
        self.ru_name = "ru_name"
        self.user_id = "789473423"
        self.schema_name = "1_0000"
        self.feedback_count = 1
        self.display_address = "68 Abingdon Road, Goathill"
        self.form_type = "I"
        self.collection_exercise_sid = "test-sid"
        self.case_id = "case_id"
        self.survey_id = "021"
        self.data_version = "0.0.3"
        self.feedback_type = "Feedback type"
        self.feedback_text = "Feedback text"
        self.feedback_type_question_category = "Feedback type question category"

        self.session_data = SessionData(
            tx_id=self.tx_id,
            schema_name=self.schema_name,
            response_id=self.response_id,
            period_str=self.period_str,
            language_code=None,
            launch_language_code=None,
            survey_url=None,
            ru_name=self.ru_name,
            ru_ref=self.ru_ref,
            case_id=self.case_id,
            feedback_count=self.feedback_count,
        )
        self.session_store = SessionStore("user_ik", "pepper", "eq_session_id")
        self.expires_at = datetime.now(timezone.utc) + timedelta(seconds=5)

        questionnaire = {"survey_id": self.survey_id, "data_version": self.data_version}
        self.questionnaire_schema = QuestionnaireSchema(questionnaire)

        self.metadata = {
            "tx_id": self.tx_id,
            "user_id": self.user_id,
            "schema_name": self.schema_name,
            "collection_exercise_sid": self.collection_exercise_sid,
            "period_id": self.period_id,
            "period_str": self.period_str,
            "ref_p_start_date": self.ref_p_start_date,
            "ref_p_end_date": self.ref_p_end_date,
            "ru_ref": self.ru_ref,
            "response_id": self.response_id,
            "form_type": self.form_type,
            "display_address": self.display_address,
        }

    def test_feedback_payload_with_feedback_type_question_category(self):
        feedback_payload = FeedbackPayload(
            self.metadata,
            self.session_store,
            self.questionnaire_schema,
            self.session_data.feedback_count,
            self.feedback_text,
            self.feedback_type,
            self.feedback_type_question_category,
        )

        actual_payload = feedback_payload()

        expected_payload = {
            "collection": {
                "exercise_sid": self.collection_exercise_sid,
                "period": self.period_id,
                "schema_name": self.schema_name,
            },
            "data": {
                "feedback_count": self.feedback_count,
                "feedback_text": self.feedback_text,
                "feedback_type": self.feedback_type,
                "feedback_type_question_category": self.feedback_type_question_category,
            },
            "form_type": self.form_type,
            "launch_language_code": "en",
            "metadata": {
                "display_address": self.display_address,
                "ref_period_end_date": self.ref_p_end_date,
                "ref_period_start_date": self.ref_p_start_date,
                "ru_ref": self.ru_ref,
                "user_id": self.user_id,
            },
            "origin": "uk.gov.ons.edc.eq",
            "submitted_at": actual_payload["submitted_at"],
            "survey_id": self.survey_id,
            "tx_id": self.tx_id,
            "type": "uk.gov.ons.edc.eq:feedback",
            "version": self.data_version,
        }

        assert actual_payload == expected_payload

    def test_feedback_payload_without_feedback_type_question_category(self):
        feedback_payload = FeedbackPayload(
            self.metadata,
            self.session_store,
            self.questionnaire_schema,
            self.session_data.feedback_count,
            self.feedback_text,
            self.feedback_type,
        )

        actual_payload = feedback_payload()

        expected_payload = {
            "collection": {
                "exercise_sid": self.collection_exercise_sid,
                "period": self.period_id,
                "schema_name": self.schema_name,
            },
            "data": {
                "feedback_count": self.feedback_count,
                "feedback_text": self.feedback_text,
                "feedback_type": self.feedback_type,
            },
            "form_type": self.form_type,
            "launch_language_code": "en",
            "metadata": {
                "display_address": self.display_address,
                "ref_period_end_date": self.ref_p_end_date,
                "ref_period_start_date": self.ref_p_start_date,
                "ru_ref": self.ru_ref,
                "user_id": self.user_id,
            },
            "origin": "uk.gov.ons.edc.eq",
            "submitted_at": actual_payload["submitted_at"],
            "survey_id": self.survey_id,
            "tx_id": self.tx_id,
            "type": "uk.gov.ons.edc.eq:feedback",
            "version": self.data_version,
        }

        assert actual_payload == expected_payload

    def test_feedback_metadata(self):
        feedback_metadata = FeedbackMetadata(
            self.feedback_count, self.form_type, "cy", "GB-ENG", self.tx_id
        )

        expected_metadata = {
            "feedback_count": self.feedback_count,
            "feedback_submission_date": datetime.now(tz=timezone.utc).strftime(
                "%Y-%m-%d"
            ),
            "form_type": self.form_type,
            "language_code": "cy",
            "region_code": "GB-ENG",
            "tx_id": self.tx_id,
        }

        assert feedback_metadata() == expected_metadata
