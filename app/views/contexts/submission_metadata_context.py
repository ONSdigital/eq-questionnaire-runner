from datetime import datetime

from flask_babel import format_datetime, lazy_gettext

from app.libs.utils import convert_tx_id


def build_submission_metadata_context(
    survey_type: str, submitted_at: datetime, tx_id: str
) -> dict:
    submitted_on = {
        "term": lazy_gettext("Submitted on:"),
        "descriptions": [
            {
                "description": lazy_gettext(
                    "{date} at {time}".format(
                        date=format_datetime(submitted_at, format="dd LLLL yyyy"),
                        time=format_datetime(submitted_at, format="HH:mm"),
                    )
                )
            }
        ],
    }
    submission_reference = {
        "term": lazy_gettext("Submission reference:"),
        "descriptions": [
            {"description": " - ".join(convert_tx_id(tx_id).upper().split("-"))}
        ],
    }
    if survey_type == "social":
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
