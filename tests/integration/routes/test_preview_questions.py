from app.utilities.json import json_loads
from tests.integration.integration_test_case import IntegrationTestCase


class TestSchema(IntegrationTestCase):
    def test_get_preview_questions_flag(self):
        self.get("/schemas/test_preview_questions")
        response = self.getResponseData()
        parsed_json = json_loads(response)

        self.assertIn("preview_questions", parsed_json)
        self.assertEqual(parsed_json["preview_questions"], True)

    def test_preview_questions(self):
        self.launchSurvey("test_preview_questions")
        self.get("/questionnaire/preview")

        self.assertStatusCode(200)
        self.assertInUrl("preview")
