from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import SUBMIT_URL_PATH, THANK_YOU_URL_PATH


class TestQuestionnaireQuestionDefinition(IntegrationTestCase):
    def test_question_definition(self):
        # Given I launch a questionnaire with definitions
        self.launchSurveyV2(schema_name="test_question_definition")

        # When I start the survey I am presented with the definitions title and content correctly
        self.assertInBody(
            "Do you connect a LiFePO4 battery to your <em>photovoltaic system</em> to store surplus energy?"
        )

        self.assertInBody("What is a photovoltaic system?")
        self.assertInBody(
            "A typical photovoltaic system employs solar panels, each comprising a number of solar cells, "
            "which generate electrical power. PV installations may be ground-mounted, rooftop mounted or wall mounted. "
            "The mount may be fixed, or use a solar tracker to follow the sun across the sky."
        )

        # When we continue we go to the summary page
        self.post()
        self.assertInUrl(SUBMIT_URL_PATH)

        # And Submit my answers
        self.post()
        self.assertInUrl(THANK_YOU_URL_PATH)
