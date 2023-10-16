import pytest

from app.questionnaire.return_location import ReturnLocation


@pytest.mark.usefixtures("app")
def test_location_url():
    return_location = ReturnLocation(
        return_to="test-return-to",
        return_to_block_id="test-return-to-block-id",
        return_to_answer_id="test-return-to-answer-id",
        return_to_list_name="test-return-to-list-name",
        return_to_list_item_id="return-to-list-item-id",
    )

    assert return_location.to_dict() == {
        "return_to": "test-return-to",
        "return_to_block_id": "test-return-to-block-id",
        "return_to_answer_id": "test-return-to-answer-id",
        "return_to_list_name": "test-return-to-list-name",
        "return_to_list_item_id": "return-to-list-item-id",
    }
