from tests.integration.integration_test_case import IntegrationTestCase


class TestOpenRadio(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.launchSurvey("test_radio_open")

    def test_label_appears(self):
        self.assertInBody("Enter your favourite drink")


class TestOpenCheckbox(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.launchSurvey("test_radio_open_checkbox")

    def test_label_doesnt_appear(self):
        self.assertInBody("Enter your favourite drink")
