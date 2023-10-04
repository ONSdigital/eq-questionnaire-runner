import pytest

from app.views.contexts.summary.answer import Answer


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "return_to, return_to_block_id, is_in_repeating_section",
    [
        ("section-summary", None, False),
        (None, None, False),
        ("calculated-summary", "total", False),
        ("section-summary", None, True),
        (None, None, True),
        ("calculated-summary", "total", True),
    ],
)
def test_create_answer(return_to, return_to_block_id, is_in_repeating_section):
    answer = Answer(
        answer_schema={"id": "answer-id", "label": "Answer Label", "type": "date"},
        answer_value="An answer",
        block_id="house-type",
        list_name="answer-list",
        list_item_id="answer-item-id",
        return_to=return_to,
        return_to_block_id=return_to_block_id,
        return_to_list_item_id=None,
        is_in_repeating_section=is_in_repeating_section,
    )

    assert answer.id == "answer-id"
    assert answer.label == "Answer Label"
    assert answer.value == "An answer"
    assert answer.type == "date"

    return_to_answer_id = answer.id
    if not is_in_repeating_section:
        return_to_answer_id += "-answer-item-id"

    if return_to and return_to_block_id:
        query_string = f"?return_to={return_to}&return_to_answer_id={return_to_answer_id}&return_to_block_id={return_to_block_id}"
    elif return_to:
        query_string = (
            f"?return_to={return_to}&return_to_answer_id={return_to_answer_id}"
        )
    else:
        query_string = ""

    assert (
        answer.link
        == f"/questionnaire/answer-list/answer-item-id/house-type/{query_string}#{answer.id}"
    )


@pytest.mark.usefixtures("app")
def test_date_answer_type():
    # When
    answer = Answer(
        answer_schema={"id": "answer-id", "label": "", "type": "date"},
        answer_value=None,
        block_id="house-type",
        list_name="answer-list",
        list_item_id="answer-item-id",
        return_to="section-summary",
        return_to_block_id=None,
        return_to_list_item_id=None,
        is_in_repeating_section=False,
    )

    # Then
    assert answer.type == "date"
