from mock import patch

from tests.integration.integration_test_case import IntegrationTestCase


class TestNoQuestionnaireState(IntegrationTestCase):
    def test_questionnaire_route_before_questionnaire_submitted(self):
        # Given
        self.launchSurvey("test_view_submitted_response")

        # When
        with patch("app.routes.questionnaire.get_metadata", return_value=None):
            self.post()

            # Then
            self.assertStatusUnauthorised()

    def test_questionnaire_route_after_questionnaire_submitted(self):
        # Given
        self.launchSurvey("test_view_submitted_response")
        self.post()
        self.post()
        self.post()

        # When
        with patch("app.routes.questionnaire.get_metadata", return_value=None):
            self.get("/questionnaire/name/")

            # Then
            self.assertStatusUnauthorised()
            self.assertInBody("Your questionnaire has been submitted")

    def test_post_submission_route_before_questionnaire_submitted(self):
        # Given
        self.launchSurvey("test_view_submitted_response")

        # When
        with patch("app.routes.questionnaire.get_metadata", return_value=None):
            self.get("/submitted/view-response")

            # Then
            self.assertStatusUnauthorised()

    def test_post_submission_route_after_questionnaire_submitted(self):
        # Given
        self.launchSurvey("test_view_submitted_response")
        self.post()
        self.post()
        self.post()

        # When
        with patch("app.routes.questionnaire.get_metadata", return_value=None):
            self.get("/submitted/view-response")

            # Then
            self.assertStatusUnauthorised()
            self.assertInBody("Your questionnaire has been submitted")
