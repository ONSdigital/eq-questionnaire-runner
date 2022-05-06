import pytest

from app.views.contexts.summary.answer import Answer


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "return_to, return_to_block_id",
    [("section-summary", None), (None, None)],
)
def test_create_answer(return_to, return_to_block_id):
    answer = Answer(
        answer_schema={"id": "answer-id", "label": "Answer Label", "type": "date"},
        answer_value="An answer",
        block_id="house-type",
        list_name="answer-list",
        list_item_id="answer-item-id",
        return_to=return_to,
        return_to_block_id=return_to_block_id,
    )

    assert answer.id == "answer-id"
    assert answer.label == "Answer Label"
    assert answer.value == "An answer"
    assert answer.type == "date"

    query_string = (
        "?return_to=section-summary&return_to_answer_id=answer-id" if return_to else ""
    )
    assert (
        answer.link
        == f"/questionnaire/answer-list/answer-item-id/house-type/{query_string}#answer-id"
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
    )

    # Then
    assert answer.type == "date"
