import json

from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireListChangeEvaluatesSections(IntegrationTestCase):
    def get_selected_radio_button_value(self):
        try:
            selected = self.getHtmlSoup().find_all(
                'input', {'class': 'radio__input', 'checked': True}
            )
            return selected[0].get('value')
        except IndexError:
            return None

    def test_happy_path(self):
        self.launchSurvey('test_radio_mandatory', roles=['dumper'])

        self.assertEqualUrl('/questionnaire/radio-mandatory/')

        self.post({'radio-mandatory-answer': 'Coffee'})
        self.assertEqualUrl('/questionnaire/summary/')

        self.get('/questionnaire/radio-mandatory')
        selected = self.get_selected_radio_button_value()

        self.assertEqualUrl('/questionnaire/radio-mandatory')
        self.assertEqual(selected, 'Coffee')

        self.post({'radio-mandatory-answer': ''})

        self.assertEqualUrl('/questionnaire/radio-mandatory')

        selected = self.get_selected_radio_button_value()
        self.assertIsNone(selected)

        self.get('/dump/debug')
        response = json.loads(self.getResponseData())
        self.assertListEqual(response['ANSWERS'], [])
