from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnairePlurals(IntegrationTestCase):
    def test_plural_page(self):
        self.launchSurvey("test_plural_forms")

        self.post({"number-of-people-answer": 0})

        self.assertEqualPageTitle("… people live here, is this correct? - Census 2021")
        self.assertInBody("0 people live here, is this correct?")
        self.assertInBody("Yes, 0 people live here")

        # Continue check question and answer on summary
        self.post()
        self.assertInBody("0 people live here, is this correct?")
        self.assertInBody("Yes, 0 people live here")
