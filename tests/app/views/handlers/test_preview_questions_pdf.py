import pytest

from app.data_models import QuestionnaireStore
from app.views.contexts.preview_context import PreviewNotEnabledException
from app.views.handlers.preview_questions_pdf import PreviewQuestionsPDF
from tests.app.views.handlers.conftest import set_storage_data


@pytest.mark.usefixtures("app")
def test_preview_questions_disabled_raises_exception(storage, schema, language):
    set_storage_data(storage)

    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.set_metadata({"schema_name": "test_checkbox"})
    with pytest.raises(PreviewNotEnabledException):
        PreviewQuestionsPDF(schema, questionnaire_store, language).get_context()
