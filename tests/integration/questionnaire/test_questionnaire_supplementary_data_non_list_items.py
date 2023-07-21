from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireSupplementaryDataNonListItems(IntegrationTestCase):
    def test_supplementary_data_non_list_items(self):
        self.launchSupplementaryDataSurvey(
            "test_supplementary_data_non_list_items",
            sds_dataset_id="693dc252-2e90-4412-bd9c-c4d953e36fcd",
            ru_ref="12346789012A",
            survey_id="123",
        )
        self.post()
        self.post()
        self.post({"same-email-answer": "Yes"})

        # supplementary data can be used for validation
        self.post({"sales-bristol-answer": "444000", "sales-london-answer": "222000"})
        self.assertInBody("Enter answers that add up to or are less than 555,000")

        # a calculated sum equal to the supplementary data value should be allowed and show correctly
        self.post({"sales-bristol-answer": "444000", "sales-london-answer": "111000"})
        self.assertInBody(
            "Total value of sales from Bristol and London is calculated to be £555,000.00. Is this correct?"
        )
        self.post()

        # all supplementary data values can be piped into the interstitial block
        self.assertInBody("<strong>Telephone Number</strong>: 01174564561")
        self.assertInBody("<strong>Email</strong>: contact@lidl.org")
        self.assertInBody("<strong>Note Title</strong>: Value of total sales")
        self.assertInBody("<strong>Note Description</strong>: Total value of goods")
        self.assertInBody("<strong>Note Example Title</strong>: Includes")
        self.assertInBody(
            "<strong>Note Example Description</strong>: Sales across all EU stores"
        )
        self.assertInBody(
            "<strong>Guidance</strong>: Guidance from supplementary data for this survey"
        )
        self.assertInBody("<strong>Total Uk Sales</strong>: £555,000.00")
        self.assertInBody("<strong>Bristol sales</strong>: £444,000.00")
        self.assertInBody("<strong>London sales</strong>: £111,000.00")
        self.assertInBody(
            "<strong>Sum of Bristol and London sales</strong>: £555,000.00"
        )

        # submission
        self.post()
        self.post()
        self.assertStatusOK()
