from datetime import datetime, timezone

from app.views.handlers.feedback import FeedbackMetadata, FeedbackPayload


def test_feedback_payload():
    feedback_payload = FeedbackPayload("Feedback text", "Feedback type")
    expected_payload = {
        "feedback_text": "Feedback text",
        "feedback_type": "Feedback type",
    }

    assert feedback_payload() == expected_payload


def test_feedback_metadata():
    feedback_metadata = FeedbackMetadata(1, "H", "cy", "GB-ENG", "123")

    expected_metadata = {
        "feedback_count": 1,
        "feedback_submission_date": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
        "form_type": "H",
        "language_code": "cy",
        "region_code": "GB-ENG",
        "tx_id": "123",
    }

    assert feedback_metadata() == expected_metadata
