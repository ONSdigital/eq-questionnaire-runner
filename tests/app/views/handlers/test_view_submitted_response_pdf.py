from datetime import datetime, timedelta, timezone

import pytest

from app.data_models import QuestionnaireStore
from app.views.handlers.view_submitted_response import ViewSubmittedResponseExpired
from app.views.handlers.view_submitted_response_pdf import ViewSubmittedResponsePDF

from .conftest import set_storage_data


def test_pdf_not_downloadable(
    app, storage, schema, language  # pylint:disable=unused-argument
):
    submitted_at = datetime.now(timezone.utc) - timedelta(minutes=46)
    set_storage_data(storage, submitted_at=submitted_at)

    questionnaire_store = QuestionnaireStore(storage)

    with pytest.raises(ViewSubmittedResponseExpired):
        ViewSubmittedResponsePDF(
            schema,
            questionnaire_store,
            language,
        )


def test_filename_uses_schema_name(
    app, storage, schema, language  # pylint:disable=unused-argument
):
    submitted_at = datetime.now(timezone.utc)
    set_storage_data(storage, submitted_at=submitted_at)

    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.set_metadata({"schema_name": "test_view_submitted_response"})
    pdf = ViewSubmittedResponsePDF(schema, questionnaire_store, language)

    assert pdf.filename == "test_view_submitted_response.pdf"
