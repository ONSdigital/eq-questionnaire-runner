from pytest import xfail

from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireLanguage(IntegrationTestCase):
    """ Tests that the language selection from tokens works """

    def test_load_cy_survey(self):
        # When: load a cy survey
        self.launchSurvey("test_language", language_code="cy")
        # Then: welsh
        self.assertInBody("Rhowch enw")

    def test_load_non_existent_lang_fallback(self):
        # When: load a hindi survey
        self.launchSurvey("test_language", language_code="hi")
        # Then: Falls back to english
        self.assertInBody("First Name")

    def test_language_switch_in_flight(self):
        # load a english survey
        self.launchSurvey("test_language", language_code="en")
        # The language is english
        self.assertInBody("First Name")
        # Switch the language to welsh
        self.get("{}?language_code=cy".format(self.last_url))
        self.assertInBody("Rhowch enw")

    def test_switch_to_invalid_language(self):
        # load a english survey
        self.launchSurvey("test_language", language_code="en")
        # The language is english
        self.assertInBody("First Name")
        # Try and switch to an invalid language
        self.get("{}?language_code=hi".format(self.last_url))
        self.assertInBody("First Name")

    def test_title_placeholders_rendered_in_summary_using_correct_language(self):
        self.launchSurvey("test_language")

        self.post({"first-name": "Kevin", "last-name": "Bacon"})
        self.assertInBody("What is Kevin Bacon’s date of birth?")

        self.post(
            {
                "date-of-birth-answer-day": 1,
                "date-of-birth-answer-month": 2,
                "date-of-birth-answer-year": 1999,
            }
        )

        self.post({"number-of-people-answer": 0})

        self.post({"confirm-count": "Yes"})

        self.assertInUrl("/summary/")
        self.assertInBody("What is Kevin Bacon’s date of birth?")
        self.assertInBody("1 February 1999")

        self.get(self.last_url + "?language_code=cy")

        self.assertInUrl("/summary/?language_code=cy")
        self.assertInBody("Beth yw dyddiad geni Kevin Bacon?")
        self.assertInBody("1 Chwefror 1999")

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
                self.launchSurvey("test_language")

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

                self.post({"confirm-count": "Yes"})

                self.assertInUrl("/summary/")
                self.assertInBody(data["question_title"]["cy"])
                self.assertInBody(data["answer"]["cy"])

                self.get(self.last_url + "?language_code=en")
                self.assertInBody(data["question_title"]["en"])
                self.assertInBody(data["answer"]["en"])

    def test_error_messages(self):
        # load a welsh survey
        self.launchSurvey("test_language", language_code="cy")
        # Submit and check the error message is in Welsh
        self.post()
        xfail("Error strings have been updated, waiting for translations to be done")
        self.assertInBody("Mae 1 gwall ar y dudalen hon")
        self.assertInBody("Nodwch ateb i barhau")

    def test_contact_us_link(self):
        # load a welsh survey
        self.launchSurvey("test_language", language_code="cy")
        # Get redirected to a 404
        self.get("/not-a-page")
        self.assertInBody("https://cyfrifiad.gov.uk/cysylltu-a-ni/")
