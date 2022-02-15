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


def test_has_expired_no_submitted_at_return_false(storage, language, app):
    with app.app_context():
        set_storage_data(storage)
        questionnaire_store = QuestionnaireStore(storage)
        schema = QuestionnaireSchema({"post_submission": {"view_response": True}})
        view_submitted_response = ViewSubmittedResponse(
            schema, questionnaire_store, language
        )
        assert view_submitted_response.has_expired is False
