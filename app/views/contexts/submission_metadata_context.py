from datetime import datetime
from typing import Any

from flask_babel import format_datetime, lazy_gettext

from app.libs.utils import convert_tx_id
from app.survey_config.survey_type import SurveyType


def build_submission_metadata_context(
    survey_type: SurveyType, submitted_at: datetime, tx_id: str
) -> dict[str, Any]:
    submitted_on = {
        "term": lazy_gettext("Submitted on:"),
        "descriptions": [
            {
                "description": lazy_gettext("{date} at {time}").format(
                    date=format_datetime(submitted_at, format="dd LLLL yyyy"),
                    time=format_datetime(submitted_at, format="HH:mm"),
                )
            }
        ],
    }

    submission_reference = {
        "term": lazy_gettext("Submission reference:"),
        "descriptions": [{"description": convert_tx_id(tx_id)}],
    }
    if survey_type is SurveyType.SOCIAL:
        return {
            "data-qa": "metadata",
            "termCol": 3,
            "descriptionCol": 9,
            "itemsList": [submitted_on],
        }
    return {
        "data-qa": "metadata",
        "termCol": 5,
        "descriptionCol": 7,
        "itemsList": [submitted_on, submission_reference],
    }
