from datetime import datetime, timezone

from flask import Flask

from app.survey_config.survey_type import SurveyType
from app.views.contexts.submission_metadata_context import (
    build_submission_metadata_context,
)

SURVEY_TYPE_DEFAULT = SurveyType.DEFAULT
SURVEY_TYPE_SOCIAL = SurveyType.SOCIAL
SURVEY_TYPE_HEALTH = SurveyType.HEALTH
SUBMITTED_AT = datetime(2021, 8, 17, 10, 10, 0, tzinfo=timezone.utc)
TX_ID = "6b6f90e6-6c27-4c76-8295-7a14e2c4a399"


def test_metadata_survey_type_social(app: Flask):
    with app.app_context():
        metadata = build_submission_metadata_context(
            SURVEY_TYPE_SOCIAL, SUBMITTED_AT, TX_ID
        )
        assert len(metadata["itemsList"]) == 1
        assert metadata["data-qa"] == "metadata"
        assert metadata["termCol"] == 3
        assert metadata["descriptionCol"] == 9
        assert metadata["itemsList"][0] == {
            "descriptions": [{"description": "17 August 2021 at 11:10"}],
            "term": "Submitted on:",
        }


def test_metadata_survey_type_health(app: Flask):
    with app.app_context():
        metadata = build_submission_metadata_context(
            SURVEY_TYPE_HEALTH, SUBMITTED_AT, TX_ID
        )
        assert len(metadata["itemsList"]) == 1
        assert metadata["data-qa"] == "metadata"
        assert metadata["termCol"] == 3
        assert metadata["descriptionCol"] == 9
        assert metadata["itemsList"][0] == {
            "descriptions": [{"description": "17 August 2021 at 11:10"}],
            "term": "Submitted on:",
        }


def test_metadata_survey_type_default(app: Flask):
    with app.app_context():
        metadata = build_submission_metadata_context(
            SURVEY_TYPE_DEFAULT, SUBMITTED_AT, TX_ID
        )
        assert metadata["data-qa"] == "metadata"
        assert len(metadata["itemsList"]) == 2
        assert metadata["termCol"] == 5
        assert metadata["descriptionCol"] == 7
        assert metadata["itemsList"][0] == {
            "descriptions": [{"description": "17 August 2021 at 11:10"}],
            "term": "Submitted on:",
        }
        assert metadata["itemsList"][1] == {
            "descriptions": [{"description": "6B6F - 90E6 - 6C27 - 4C76"}],
            "term": "Submission reference:",
        }
