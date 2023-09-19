from datetime import datetime, timedelta, timezone

import pytest
from freezegun import freeze_time

from app.data_models import QuestionnaireStore
from app.views.handlers.view_submitted_response import ViewSubmittedResponseExpired
from app.views.handlers.view_submitted_response_pdf import ViewSubmittedResponsePDF
from tests.app.views.handlers.conftest import set_storage_data


@pytest.mark.usefixtures("app")
def test_pdf_not_downloadable(storage, schema, language):
    submitted_at = datetime.now(timezone.utc) - timedelta(minutes=46)
    set_storage_data(storage, submitted_at=submitted_at)

    questionnaire_store = QuestionnaireStore(storage)

    with pytest.raises(ViewSubmittedResponseExpired):
        ViewSubmittedResponsePDF(
            schema,
            questionnaire_store,
            language,
        )


@pytest.mark.usefixtures("app")
@freeze_time("2022-06-01T15:34:54+00:00")
def test_filename_uses_schema_name(storage, schema, language):
    submitted_at = datetime.now(timezone.utc)
    set_storage_data(storage, submitted_at=submitted_at)

    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.set_metadata({"schema_name": "test_view_submitted_response"})
    pdf = ViewSubmittedResponsePDF(schema, questionnaire_store, language)

    assert pdf.filename == "test-schema-view-submitted-response-2022-06-01.pdf"
