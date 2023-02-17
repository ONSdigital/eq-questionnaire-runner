from datetime import datetime, timezone
from io import BytesIO

import flask
import pytest
from freezegun import freeze_time
from mock import Mock

from app.data_models import QuestionnaireStore
from app.views.handlers.view_preview_questions_pdf import ViewPreviewQuestionsPDF

from .conftest import set_storage_data


@pytest.mark.usefixtures("app")
@freeze_time("2022-06-01T15:34:54+00:00")
def test_filename_uses_schema_name(storage, schema, language):
    submitted_at = datetime.now(timezone.utc)
    set_storage_data(storage, submitted_at=submitted_at)

    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.set_metadata(
        {"schema_name": "test_introduction_preview_linear_schema"}
    )
    pdf = ViewPreviewQuestionsPDF(schema, questionnaire_store, language)

    assert pdf.filename == "test-schema-view-submitted-response-2022-06-01.pdf"


@pytest.mark.usefixtures("app")
@freeze_time("2022-06-01T15:34:54+00:00")
def test_get_pdf_returns_bytes(storage, schema, language):
    flask.globals.request.csp_nonce = Mock()
    submitted_at = datetime.now(timezone.utc)
    set_storage_data(storage, submitted_at=submitted_at)

    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.set_metadata(
        {"schema_name": "test_introduction_preview_linear_schema"}
    )
    pdf = ViewPreviewQuestionsPDF(schema, questionnaire_store, language)

    assert isinstance(pdf.get_pdf(), BytesIO)
