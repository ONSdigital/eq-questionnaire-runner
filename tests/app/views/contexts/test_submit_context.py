from unittest.mock import Mock, patch

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
from app.utilities.schema import load_schema_from_name
from app.views.contexts import SubmitQuestionnaireContext
from tests.app.app_context_test_case import AppContextTestCase
from tests.app.views.contexts import SummaryContextTestCase


class SubmitContextTestCase(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.language = "en"
        self.metadata = {}
        self.response_metadata = {}
        self.answer_store = AnswerStore()
        self.list_store = ListStore()
        self.progress_store = ProgressStore()


# pylint: disable=attribute-defined-outside-init
class TestSubmitContext(SubmitContextTestCase):
    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
    def test_default_submission_content(self):
        self.schema = load_schema_from_name("test_instructions")
        submission_content = self.schema.get_submission()
        self.assertEqual(submission_content, {})

        submit_questionnaire_context = SubmitQuestionnaireContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
            self.response_metadata,
        )

        context = submit_questionnaire_context()

        self.assertEqual(context["title"], "Check your answers and submit")
        self.assertEqual(
            context["guidance"], "Please submit this survey to complete it"
        )
        self.assertIsNone(context["warning"])
        self.assertEqual(context["submit_button"], "Submit answers")

    def test_custom_submission_content(self):
        self.schema = load_schema_from_name("test_submit_with_custom_submission_text")
        submit_questionnaire_context = SubmitQuestionnaireContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
            self.response_metadata,
        )

        context = submit_questionnaire_context()

        self.assertEqual(context["title"], "Submit your questionnaire")
        self.assertEqual(
            context["guidance"],
            "Thank you for your answers, submit this to complete it",
        )
        self.assertEqual(
            context["warning"], "You cannot view your answers after submission"
        )
        self.assertEqual(context["submit_button"], "Submit")

    def test_summary_context_not_built_when_no_summary(self):
        self.schema = load_schema_from_name("test_submit_with_custom_submission_text")
        submit_questionnaire_context = SubmitQuestionnaireContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
            self.response_metadata,
        )

        context = submit_questionnaire_context()

        self.assertNotIn("summary", context)


class TestSubmitContextWithSummary(SubmitContextTestCase, SummaryContextTestCase):
    def test_context(self):
        self.schema = load_schema_from_name("test_submit_with_summary")
        submit_questionnaire_context = SubmitQuestionnaireContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
            self.response_metadata,
        )

        context = submit_questionnaire_context()
        self.assert_summary_context(context)
