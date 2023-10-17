import pytest

from app.questionnaire.return_location import ReturnLocation


def test_return_location_to_dict():
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


def test_return_location_to_dict_with_anchor_return_to_answer_id():
    return_location = ReturnLocation(
        return_to="test-return-to",
        return_to_block_id="test-return-to-block-id",
        return_to_answer_id="test-return-to-answer-id",
        return_to_list_name="test-return-to-list-name",
        return_to_list_item_id="return-to-list-item-id",
    )

    assert return_location.to_dict(anchor_return_to_answer_id=True) == {
        "return_to": "test-return-to",
        "return_to_block_id": "test-return-to-block-id",
        "_anchor": "test-return-to-answer-id",
        "return_to_list_name": "test-return-to-list-name",
        "return_to_list_item_id": "return-to-list-item-id",
    }
