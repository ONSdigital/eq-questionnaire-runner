from tests.integration.integration_test_case import IntegrationTestCase


class TestOpenRadio(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.launchSurvey("test_radio_detail_answer_open")

    def test_label_appears(self):
        self.assertInBody("Enter your favourite drink")
