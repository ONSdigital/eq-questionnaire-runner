import pytest

from app.data_models import QuestionnaireStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.handlers.view_submitted_response import (
    ViewSubmittedResponse,
    ViewSubmittedResponseNotEnabled,
)
from tests.app.views.handlers.conftest import set_storage_data


def test_not_enabled(storage, language):
    set_storage_data(storage)
    questionnaire_store = QuestionnaireStore(storage)

    with pytest.raises(ViewSubmittedResponseNotEnabled):
        ViewSubmittedResponse(QuestionnaireSchema({}), questionnaire_store, language)
