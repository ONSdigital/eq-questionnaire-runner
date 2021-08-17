from datetime import datetime, timezone

from flask import Flask

from app.views.contexts.submission_metadata_context import (
    build_submission_metadata_context,
)

SURVEY_TYPE_DEFAULT = "default"
SURVEY_TYPE_SOCIAL = "social"
SUBMITTED_AT = datetime(2021, 8, 17, 10, 10, 0, tzinfo=timezone.utc)
TX_ID = "6b6f90e6-6c27-4c76-8295-7a14e2c4a399"


def test_metadata_survey_type_social(app: Flask):
    with app.app_context():
        metadata = build_submission_metadata_context(
            SURVEY_TYPE_SOCIAL, SUBMITTED_AT, TX_ID
        )
        assert len(metadata) == 1
        assert (
            str(metadata)
            == "[{'term': l'Submitted on:', 'descriptions': [{'description': '17 August 2021 11:10'}]}]"
        )


def test_metadata_survey_type_default(app: Flask):
    with app.app_context():
        metadata = build_submission_metadata_context(
            SURVEY_TYPE_DEFAULT, SUBMITTED_AT, TX_ID
        )
        assert len(metadata) == 2
        assert (
            str(metadata)
            == "[{'term': l'Submitted on:', 'descriptions': [{'description': '17 August 2021 11:10'}]}, {'term': l'Submission reference:', 'descriptions': [{"
            "'description': '6b6f-90e6-6c27-4c76'}]}] "
        )
