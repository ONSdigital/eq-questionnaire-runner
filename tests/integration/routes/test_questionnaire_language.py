from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireLanguage(IntegrationTestCase):
    """Tests that the language selection from tokens works"""

    def test_load_cy_survey(self):
        # When: load a cy survey
        self.launchSurveyV2(schema_name="test_language", language_code="cy")
        # Then: welsh
        self.post()
        self.assertInBody("Rhowch enw")

    def test_load_non_existent_lang_fallback(self):
        # When: load a hindi survey
        self.launchSurveyV2(schema_name="test_language", language_code="hi")
        # Then: Falls back to english
        self.post()
        self.assertInBody("First Name")

    def test_language_switch_in_flight(self):
        # load a english survey
        self.launchSurveyV2(schema_name="test_language", language_code="en")
        # The language is english
        self.post()
        self.assertInBody("First Name")
        # Switch the language to welsh
        self.get(f"{self.last_url}?language_code=cy")
        self.assertInBody("Rhowch enw")

    def test_switch_to_invalid_language(self):
        # load a english survey
        self.launchSurveyV2(schema_name="test_language", language_code="en")
        # The language is english
        self.post()
        self.assertInBody("First Name")
        # Try and switch to an invalid language
        self.get(f"{self.last_url}?language_code=hi")
        self.assertInBody("First Name")

    def test_plural_forms_rendered_using_correct_language(self):
        test_data_sets = [
            {
                "count": 0,
                "question_title": {
                    "en": "0 people live here, is this correct?",
                    "cy": "Mae 0 person yn byw yma, ydy hyn yn gywir? (zero)",
                },
                "answer": {
                    "en": "Yes, 0 people live here",
                    "cy": "Ydy, mae 0 person yn byw yma (zero)",
                },
            },
            {
                "count": 1,
                "question_title": {
                    "en": "1 person lives here, is this correct?",
                    "cy": "Mae 1 person yn byw yma, ydy hyn yn gywir? (one)",
                },
                "answer": {
                    "en": "Yes, 1 person lives here",
                    "cy": "Ydy, mae 1 person yn byw yma (one)",
                },
            },
            {
                "count": 2,
                "question_title": {
                    "en": "2 people live here, is this correct?",
                    "cy": "Mae 2 person yn byw yma, ydy hyn yn gywir? (two)",
                },
                "answer": {
                    "en": "Yes, 2 people live here",
                    "cy": "Ydy, mae 2 person yn byw yma (two)",
                },
            },
            {
                "count": 3,
                "question_title": {
                    "en": "3 people live here, is this correct?",
                    "cy": "Mae 3 pherson yn byw yma, ydy hyn yn gywir? (few)",
                },
                "answer": {
                    "en": "Yes, 3 people live here",
                    "cy": "Ydy, mae 3 pherson yn byw yma (few)",
                },
            },
            {
                "count": 6,
                "question_title": {
                    "en": "6 people live here, is this correct?",
                    "cy": "Mae 6 pherson yn byw yma, ydy hyn yn gywir? (many)",
                },
                "answer": {
                    "en": "Yes, 6 people live here",
                    "cy": "Ydy, mae 6 pherson yn byw yma (many)",
                },
            },
            {
                "count": 4,
                "question_title": {
                    "en": "4 people live here, is this correct?",
                    "cy": "Mae 4 pherson yn byw yma, ydy hyn yn gywir? (other)",
                },
                "answer": {
                    "en": "Yes, 4 people live here",
                    "cy": "Ydy, mae 4 pherson yn byw yma (other)",
                },
            },
            {
                "count": 5,
                "question_title": {
                    "en": "5 people live here, is this correct?",
                    "cy": "Mae 5 pherson yn byw yma, ydy hyn yn gywir? (other)",
                },
                "answer": {
                    "en": "Yes, 5 people live here",
                    "cy": "Ydy, mae 5 pherson yn byw yma (other)",
                },
            },
            {
                "count": 10,
                "question_title": {
                    "en": "10 people live here, is this correct?",
                    "cy": "Mae 10 pherson yn byw yma, ydy hyn yn gywir? (other)",
                },
                "answer": {
                    "en": "Yes, 10 people live here",
                    "cy": "Ydy, mae 10 pherson yn byw yma (other)",
                },
            },
        ]
        for data in test_data_sets:
            with self.subTest(data=data):
                self.setUp()
                self.launchSurveyV2(schema_name="test_language")

                self.post()
                self.post({"first-name": "Kevin", "last-name": "Bacon"})

                self.post(
                    {
                        "date-of-birth-answer-day": 1,
                        "date-of-birth-answer-month": 2,
                        "date-of-birth-answer-year": 1999,
                    }
                )

                self.post({"number-of-people-answer": data["count"]})
                self.assertInBody(data["question_title"]["en"])
                self.assertInBody(data["answer"]["en"])

                self.get(self.last_url + "?language_code=cy")
                self.assertInBody(data["question_title"]["cy"])
                self.assertInBody(data["answer"]["cy"])

    def test_error_messages(self):
        # load a welsh survey
        self.launchSurveyV2(schema_name="test_language", language_code="cy")
        # Submit and check the error message is in Welsh
        self.post()
        self.post()
        self.assertInBody("Mae problem gyda'ch ateb")
        self.assertInBody("Rhowch ateb")

    def test_language_switch_hub_submission(self):
        # load an English survey
        self.launchSurveyV2(schema_name="test_language", language_code="en")

        # Complete the survey
        self.post()
        self.post({"first-name": "John", "last-name": "Smith"})
        self.post(
            {
                "date-of-birth-answer-day": 1,
                "date-of-birth-answer-month": 2,
                "date-of-birth-answer-year": 1999,
            }
        )
        self.post({"number-of-people-answer": 1})
        self.post({"confirm-count": "Yes"})

        # Check the custom hub text is in English
        self.assertInBody("Submission title")
        self.assertInBody("Submission warning")
        self.assertInBody("Submission guidance")
        self.assertInBody("Submission button")

        # Switch language to Welsh
        self.get(self.last_url + "?language_code=cy")

        # Check the custom hub text is in Welsh
        self.assertInBody("Teitl cyflwyno")
        self.assertInBody("Rhybudd cyflwyno")
        self.assertInBody("Canllawiau cyflwyno")
        self.assertInBody("Botwm cyflwyno")

    def test_last_viewed_guidance_is_displayed_after_language_switch(self):
        # load a welsh survey
        self.launchSurveyV2(schema_name="test_language", language_code="en")
        self.post()
        self.post({"first-name": "John", "last-name": "Smith"})

        # Resume the survey and check the last viewed guidance is being displayed
        self.get("/questionnaire/dob-block/?resume=True")
        self.assertInBody("This is the last viewed question in this section")

        # Switch the language to welsh and check that the last viewed guidance is still being displayed (in welsh)
        self.get(f"{self.last_url}&language_code=cy")
        self.assertInBody("Dyma'r cwestiwn a gafodd ei weld ddiwethaf yn yr adran hon")

    def test_sign_out_cy_survey(self):
        # When: load a cy survey
        self.launchSurveyV2(schema_name="test_language", language_code="cy")
        # Then: sign out
        self.get(self.getSignOutButton()["href"], follow_redirects=True)
        # Check the text and logos are in Welsh
        self.assertInBody("Mae eich cynnydd wedi'i gadw")
        self.assertInBody("Swyddfa Ystadegau Gwladol")
