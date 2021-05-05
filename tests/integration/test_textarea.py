import json

from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import SUBMIT_URL_PATH, THANK_YOU_URL_PATH

with open("tests/fixtures/blns.json") as blns:
    NAUGHTY_STRINGS = json.load(blns)


class TestTextArea(IntegrationTestCase):
    def test_empty_submission(self):
        self.launchSurvey("test_textarea")
        self.post()

        self.assertInBody("No answer provided")

        self.post()
        self.assertInUrl(THANK_YOU_URL_PATH)

    def test_too_many_characters(self):
        self.launchSurvey("test_textarea")
        self.post({"answer": "This is longer than twenty characters"})

        self.assertInBody(
            "You have entered too many characters. Enter up to 20 characters"
        )

    def test_acceptable_submission(self):
        self.launchSurvey("test_textarea")
        self.post({"answer": "Less than 20 chars"})

        self.assertInBody("Less than 20 chars")

        self.post()
        self.assertInUrl(THANK_YOU_URL_PATH)

    def test_big_list_of_naughty_strings(self):
        self.launchSurvey("test_big_list_naughty_strings")

        answers = {}
        for counter, value in enumerate(NAUGHTY_STRINGS):
            key = "answer{}".format(counter)
            answers[key] = value
        self.post(answers)
        self.assertInUrl(SUBMIT_URL_PATH)
        self.assertEqual(200, self.last_response.status_code)
