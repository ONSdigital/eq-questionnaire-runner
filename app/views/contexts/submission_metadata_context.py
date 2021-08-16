from datetime import datetime

from flask_babel import format_datetime, lazy_gettext

from app.libs.utils import convert_tx_id


def build_submission_metadata_context(
    survey_type: str, submitted_at: datetime, tx_id: str
) -> list:
    submitted_on = {
        "term": lazy_gettext("Submitted on:"),
        "descriptions": [
            {"description": format_datetime(submitted_at, format="dd LLLL yyyy HH:mm")}
        ],
    }
    submission_reference = {
        "term": lazy_gettext("Submission reference:"),
        "descriptions": [{"description": convert_tx_id(tx_id)}],
    }
    if survey_type == "social":
        return [submitted_on]
    return [submitted_on, submission_reference]
