from tests.app.app_context_test_case import AppContextTestCase


class TestSummaryContextHelper(AppContextTestCase):
    def check_context(self, context):
        self.assertEqual(len(context), 1)
        self.assertTrue("summary" in context, "Key value summary missing from context")

        summary_context = context["summary"]
        for key_value in ("groups", "answers_are_editable", "summary_type"):
            self.assertTrue(
                key_value in summary_context,
                f"Key value {key_value} missing from context['summary']",
            )

    def check_summary_context(self, summary_rendering_context):
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
