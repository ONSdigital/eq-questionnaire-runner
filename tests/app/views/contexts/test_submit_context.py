from unittest.mock import Mock, patch

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
from app.utilities.schema import load_schema_from_name
from app.views.contexts import SubmitContext
from tests.app.app_context_test_case import AppContextTestCase


class TestStandardSummaryContext(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.metadata = {
            "return_by": "2016-10-10",
            "ref_p_start_date": "2016-10-10",
            "ref_p_end_date": "2016-10-10",
            "ru_ref": "def123",
            "response_id": "abc123",
            "ru_name": "Mr Cloggs",
            "trad_as": "Samsung",
            "tx_id": "12345678-1234-5678-1234-567812345678",
            "period_str": "201610",
            "employment_date": "2016-10-10",
            "collection_exercise_sid": "789",
            "schema_name": "0000_1",
        }
        self.language = "en"
        self.answer_store = AnswerStore()
        self.list_store = ListStore()
        self.progress_store = ProgressStore()

    def check_context(self, context):
        self.assertEqual(len(context), 1)
        self.assertTrue("summary" in context, "Key value summary missing from context")

        summary_context = context["summary"]
        for key_value in ("groups", "answers_are_editable", "summary_type"):
            self.assertTrue(
                key_value in summary_context,
                f"Key value {key_value} missing from context['summary']",
            )

    def check_summary_rendering_context(self, summary_rendering_context):
        for group in summary_rendering_context["summary"]["groups"]:
            self.assertTrue("id" in group)
            self.assertTrue("blocks" in group)
            for block in group["blocks"]:
                self.assertTrue("question" in block)
                self.assertTrue("title" in block["question"])
                self.assertTrue("answers" in block["question"])
                for answer in block["question"]["answers"]:
                    self.assertTrue("id" in answer)
                    self.assertTrue("value" in answer)
                    self.assertTrue("type" in answer)

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
    def test_submit_context_with_default_submission_content(self):
        schemas = ["test_summary", "test_instructions"]
        for schema in schemas:
            with self.subTest(schema=schema):
                schema = load_schema_from_name(schema)
                submission_content = schema.get_submission()
                self.assertIsNone(submission_content)

                submit_context = SubmitContext(
                    self.language,
                    schema,
                    self.answer_store,
                    self.list_store,
                    self.progress_store,
                    self.metadata,
                )

                context = submit_context()

                self.assertEqual(context["title"], "Check your answers and submit")
                self.assertEqual(
                    context["guidance"], "Please submit this survey to complete it"
                )
                self.assertIsNone(context["warning"])
                self.assertEqual(context["submit_button"], "Submit answers")


class TestSubmitContextWithSummary(TestStandardSummaryContext):
    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_name("test_summary")

    def test_build_summary_rendering_context(self):
        submit_context = SubmitContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        context = submit_context()
        self.check_summary_rendering_context(context)

    def test_submit_context_with_custom_submission_content(self):
        self.schema = load_schema_from_name("test_summary_with_submission_text")

        submit_context = SubmitContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        context = submit_context()

        self.assertEqual(context["title"], "Submission title")
        self.assertEqual(context["guidance"], "Submission guidance")
        self.assertEqual(context["warning"], "Submission warning")
        self.assertEqual(context["submit_button"], "Submission button")


class TestSubmitContextWithoutSummary(TestStandardSummaryContext):
    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_name("test_final_confirmation")
        self.answer_store = AnswerStore()
        self.list_store = ListStore()
        self.progress_store = ProgressStore()

    def test_submit_context_with_custom_submission_content(self):
        self.schema = load_schema_from_name("test_final_confirmation")

        submit_context = SubmitContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        context = submit_context()

        self.assertEqual(context["title"], "Submit your questionnaire")
        self.assertEqual(
            context["guidance"],
            "Thank you for your answers, submit this to complete it",
        )
        self.assertEqual(
            context["warning"], "You cannot view your answers after submission"
        )
        self.assertEqual(context["submit_button"], "Submit")

    def test_summary_rendering_context_not_built(self):
        submit_context = SubmitContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        context = submit_context()

        self.assertNotIn("summary", context)
