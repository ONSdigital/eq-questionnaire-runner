from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

from werkzeug.exceptions import BadRequestKeyError

from app.data_models import QuestionnaireStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.handlers.view_submitted_response import ViewSubmittedResponseExpired
from app.views.handlers.view_submitted_response_pdf import ViewSubmittedResponsePDF
from tests.app.app_context_test_case import AppContextTestCase


class TestViewSubmittedResponsePDF(AppContextTestCase):
    def setUp(self):
        super().setUp()

        self.schema = QuestionnaireSchema({"post_submission": {"view_response": True}})
        self.language = "en"

    def set_submitted_at(self, submitted_at):
        self.storage = Mock()
        self.storage.get_user_data = Mock(return_value=("{}", 1, submitted_at))

    def test_pdf_not_downloadable(self):
        submitted_at = datetime.now(timezone.utc) - timedelta(minutes=46)
        self.set_submitted_at(submitted_at)
        self.questionnaire_store = QuestionnaireStore(self.storage)

        with self.assertRaises(ViewSubmittedResponseExpired):
            ViewSubmittedResponsePDF(
                self.schema,
                self.questionnaire_store,
                self.language,
            )

    def test_filename_schema_name(self):
        submitted_at = datetime.now(timezone.utc)
        self.set_submitted_at(submitted_at)
        self.questionnaire_store = QuestionnaireStore(self.storage)

        self.questionnaire_store.set_metadata(
            {"schema_name": "test_view_submitted_response"}
        )
        pdf = ViewSubmittedResponsePDF(
            self.schema, self.questionnaire_store, self.language
        )

        self.assertEqual(pdf.filename, "test_view_submitted_response.pdf")
