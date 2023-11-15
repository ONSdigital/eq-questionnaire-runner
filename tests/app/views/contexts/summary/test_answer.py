import pytest

from app.questionnaire.return_location import ReturnLocation
from app.views.contexts.summary.answer import Answer


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "return_to, return_to_block_id, is_in_repeating_section, return_to_answer_id, query_string",
    [
        (
            "section-summary",
            None,
            False,
            "answer-id",
            "?return_to=section-summary&return_to_answer_id=answer-id-answer-item-id,answer-id",
        ),
        (None, None, False, "answer-id", ""),
        (
            "calculated-summary",
            "total",
            False,
            "answer-id-answer-item-id",
            "?return_to=calculated-summary&return_to_answer_id=answer-id-answer-item-id,answer-id-answer-item-id&return_to_block_id=total",
        ),
        (
            "section-summary",
            None,
            True,
            "answer-id",
            "?return_to=section-summary&return_to_answer_id=answer-id,answer-id",
        ),
        (None, None, True, "answer-id-answer-item-id", ""),
        (
            "calculated-summary",
            "total",
            True,
            "answer-id",
            "?return_to=calculated-summary&return_to_answer_id=answer-id,answer-id&return_to_block_id=total",
        ),
        (
            "calculated-summary",
            "total",
            True,
            "calculated-summary-1",
            "?return_to=calculated-summary&return_to_answer_id=answer-id,calculated-summary-1&return_to_block_id=total",
        ),
    ],
)
def test_create_answer(
    return_to,
    return_to_block_id,
    is_in_repeating_section,
    return_to_answer_id,
    query_string,
):
    return_location = ReturnLocation(
        return_to=return_to,
        return_to_block_id=return_to_block_id,
        return_to_answer_id=return_to_answer_id,
    )

    answer = Answer(
        answer_schema={"id": "answer-id", "label": "Answer Label", "type": "date"},
        answer_value="An answer",
        block_id="house-type",
        list_name="answer-list",
        list_item_id="answer-item-id",
        return_location=return_location,
        is_in_repeating_section=is_in_repeating_section,
    )

    assert answer.id == "answer-id"
    assert answer.label == "Answer Label"
    assert answer.value == "An answer"
    assert answer.type == "date"

    assert (
        answer.link
        == f"/questionnaire/answer-list/answer-item-id/house-type/{query_string}#{answer.id}"
    )


@pytest.mark.usefixtures("app")
def test_date_answer_type():
    # When
    return_location = ReturnLocation(
        return_to="section-summary",
    )

    answer = Answer(
        answer_schema={"id": "answer-id", "label": "", "type": "date"},
        answer_value=None,
        block_id="house-type",
        list_name="answer-list",
        list_item_id="answer-item-id",
        return_location=return_location,
        is_in_repeating_section=False,
    )

    # Then
    assert answer.type == "date"
