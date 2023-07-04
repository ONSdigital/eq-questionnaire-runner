from . import QuestionnaireTestCase

# pylint: disable=too-many-public-methods


class TestQuestionnaireListCollectorContent(QuestionnaireTestCase):
    def get_add_someone_link(self):
        selector = "[data-qa='add-item-link']"
        selected = self.getHtmlSoup().select(selector)
        return selected[0].get("href")

    def test_happy_path(self):
        self.launchSurvey("test_list_collector_content_page")

        self.post({"any-companies-or-branches-answer": "Yes"})

        self.add_company("Tesco", "123", "No")

        self.post({"any-other-companies-or-branches-answer": "Yes"})

        self.add_company("Asda", "456", "No")

        self.post({"any-other-companies-or-branches-answer": "No"})

        self.post()

        self.post()

        self.assertEqualUrl("/questionnaire/list-collector-content/")

        self.assertInBody(
            "You have previously reported the following companies. Press continue to updated registration and trading information."
        )

        self.post()

        self.assertInUrl("/companies-repeating-block-1/")

        self.assertInBody("Give details about Tesco")

        self.post(
            {
                "registration-number-repeating-block": "123",
                "registration-date-repeating-block-day": "1",
                "registration-date-repeating-block-month": "1",
                "registration-date-repeating-block-year": "1990",
            }
        )

        self.assertInUrl("/companies-repeating-block-2/")

        self.assertInBody("Give details about how Tesco")

        self.post(
            {
                "authorised-trader-uk-radio-repeating-block": "Yes",
                "authorised-trader-eu-radio-repeating-block": "No",
            }
        )

        self.post()

        self.assertInBody("Give details about Asda")

        self.assertInUrl("/companies-repeating-block-1/")

        self.post(
            {
                "registration-number-repeating-block": "456",
                "registration-date-repeating-block-day": "1",
                "registration-date-repeating-block-month": "1",
                "registration-date-repeating-block-year": "1990",
            }
        )

        self.assertInBody("Give details about how Asda")

        self.post(
            {
                "authorised-trader-uk-radio-repeating-block": "Yes",
                "authorised-trader-eu-radio-repeating-block": "No",
            }
        )

        self.assertInBody(
            "You have previously reported the following companies. Press continue to updated registration and trading information."
        )

        self.post()

        self.assertInUrl("questionnaire/sections/section-list-collector-contents/")

        self.assertInBody("List Collector Contents")

        self.post()

        self.assertInUrl("/questionnaire/")
