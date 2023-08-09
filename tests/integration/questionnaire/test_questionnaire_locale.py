from tests.integration.integration_test_case import IntegrationTestCase


class TestSession(IntegrationTestCase):
    def test_none_language_code_defaults_to_en(self):
        # Given a questionnaire with an answer of type mass-tonne launches with no language code in the runner claims
        token = self.token_generator.create_token_with_none_language_code(
            "test_unit_patterns"
        )
        self.get(url=f"/session?token={token}")

        # Skip to the mass-tonnes answer
        self.post()
        self.post()
        self.post()
        self.post()

        # Then the cookie_session[language_code] will have defaulted to DEFAULT_LANGUAGE_CODE (en), and the tooltip will show "tonnes" not "metric tons"
        self.assertInBody("Weight Units")
        self.assertInSelector("tonnes", "[id='mass-tonne-type']")
        self.assertNotInSelector("metric tons", "[id='mass-tonne-type']")
