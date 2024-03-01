from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnairePiping(IntegrationTestCase):
    def test_given_quotes_in_answer_when_piped_into_page_then_html_escaped_quotes_on_page(
        self,
    ):
        # Given
        self.launchSurvey("test_multiple_piping")
        self.post(action="start_questionnaire")
        self.post({"address-line-1": "44 hill side"})
        self.post()

        # When
        self.post({"first-text": "Joe", "second-text": 'Bloggs "Junior"'})
        self.post()

        # Then
        self.get(self.last_url)
        self.assertStatusOK()
        # Using raw response data rather than assertInSelectorCSS as otherwise the
        # content will be unescaped by BeautifulSoup
        assert (
            'Does <strong class="ons-highlight">Joe Bloggs &#34;Junior&#34;</strong> live at <strong class="ons-highlight">44 hill side</strong>'
            in self.getResponseData()
        )

    def test_given_html_in_answer_when_piped_into_page_then_html_escaped_on_page(self):
        # Given
        self.launchSurvey("test_multiple_piping")
        self.post(action="start_questionnaire")
        self.post({"address-line-1": "44 hill side"})
        self.post()

        # When
        self.post({"first-text": "Joe", "second-text": "Bloggs <b>Junior</b>"})
        self.post()

        # Then
        self.get(self.last_url)
        self.assertStatusOK()
        # Using raw response data rather than assertInSelectorCSS as otherwise the
        # content will be unescaped by BeautifulSoup
        assert (
            'Does <strong class="ons-highlight">Joe Bloggs &lt;b&gt;Junior&lt;/b&gt;</strong> live at <strong class="ons-highlight">44 hill side</strong>'
            in self.getResponseData()
        )

    def test_given_backslash_in_answer_when_piped_into_page_then_backslash_on_page(
        self,
    ):
        # Given
        self.launchSurvey("test_multiple_piping")
        self.post(action="start_questionnaire")
        self.post({"address-line-1": "44 hill side"})
        self.post()

        # When
        self.post({"first-text": "Joe", "second-text": "Bloggs\\John Doe"})
        self.post()

        # Then
        self.get(self.last_url)
        self.assertStatusOK()
        self.assertInSelectorCSS("Joe Bloggs\\John Doe", "h1")

    def test_answer_piped_into_option(self):
        # Given
        self.launchSurvey("test_multiple_piping")
        self.post(action="start_questionnaire")
        self.post({"address-line-1": "44 hill side", "town-city": "newport"})
        self.post()

        # When
        self.post({"first-text": "Joe", "second-text": "Bloggs\\John Doe"})
        self.post()

        # Then
        self.get(self.last_url)
        self.assertStatusOK()
        self.assertInSelectorCSS(
            "44 hill side, newport", "label", {"for": "multiple-piping-answer-0"}
        )

    def test_answer_piped_into_option_on_validation_error(self):
        """Regression test to assert that the previous answer is still piped into
        the option label on the form it is rendered with a validation error
        """
        # Given
        self.launchSurvey("test_multiple_piping")
        self.post(action="start_questionnaire")
        self.post({"address-line-1": "44 hill side", "town-city": "newport"})
        self.post()
        self.post({"first-text": "Joe", "second-text": "Bloggs\\John Doe"})
        self.post()

        # When
        self.post()

        # Then
        self.assertStatusOK()
        self.assertInSelectorCSS(
            "44 hill side, newport", "label", {"for": "multiple-piping-answer-0"}
        )
