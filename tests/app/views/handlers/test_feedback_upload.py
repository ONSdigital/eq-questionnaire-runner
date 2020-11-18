from app.views.handlers.feedback import FeedbackUpload


def test_feedback_upload_with_feedback_type_question_category():
    form_data = {
        "feedback-type": "Feedback type",
        "feedback-text": "Feedback text",
        "feedback-type-question-category": "Feedback type question category",
    }

    feedback_upload = FeedbackUpload(1, "H", "cy", "GB-ENG", "123", form_data)
    expected_message = {
        "meta_data": {
            "feedback_count": 1,
            "form_type": "H",
            "language_code": "cy",
            "region_code": "GB-ENG",
            "tx_id": "123",
        },
        "payload": {
            "feedback_text": "Feedback text",
            "feedback_type": "Feedback type",
            "feedback_type_question_category": "Feedback type question category",
        },
    }

    assert feedback_upload.message == expected_message


def test_feedback_upload_without_feedback_type_question_category():
    form_data = {"feedback-type": "Feedback type", "feedback-text": "Feedback text"}

    feedback_upload = FeedbackUpload(1, "H", "cy", "GB-ENG", "123", form_data)

    expected_message = {
        "meta_data": {
            "feedback_count": 1,
            "form_type": "H",
            "language_code": "cy",
            "region_code": "GB-ENG",
            "tx_id": "123",
        },
        "payload": {"feedback_text": "Feedback text", "feedback_type": "Feedback type"},
    }

    assert feedback_upload.message == expected_message
