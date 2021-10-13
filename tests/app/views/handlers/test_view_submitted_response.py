from unittest.mock import Mock

from app.data_models import QuestionnaireStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.handlers.view_submitted_response import (
    ViewSubmittedResponse,
    ViewSubmittedResponseNotEnabled,
)
from tests.app.app_context_test_case import AppContextTestCase


class TestViewSubmittedResponse(AppContextTestCase):
    def test_not_enabled(self):
        storage = Mock()
        storage.get_user_data = Mock(return_value=("{}", 1, None))
        questionnaire_store = QuestionnaireStore(storage)

        with self.assertRaises(ViewSubmittedResponseNotEnabled):
            ViewSubmittedResponse(QuestionnaireSchema({}), questionnaire_store, "en")
