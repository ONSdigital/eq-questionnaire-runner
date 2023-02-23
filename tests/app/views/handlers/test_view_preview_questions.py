from datetime import datetime, timezone

import pytest
from freezegun import freeze_time

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.views.handlers.view_preview_questions import ViewPreviewQuestions

from .conftest import set_storage_data


@pytest.mark.usefixtures("app")
@freeze_time("2022-06-01T15:34:54+00:00")
def test_view_preview_questions_context(storage, language):
    submitted_at = datetime.now(timezone.utc)
    set_storage_data(storage, submitted_at=submitted_at)

    questionnaire_store = QuestionnaireStore(storage)
    schema = QuestionnaireSchema({"preview_questions": True})
    preview = ViewPreviewQuestions(schema, questionnaire_store, language)

    assert preview.get_context() == {
        "hide_sign_out_button": True,
        "pdf_url": "/questionnaire/download-pdf",
        "preview": {"groups": []},
    }
