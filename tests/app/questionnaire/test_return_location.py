from app.questionnaire.return_location import ReturnLocation

TEST_RETURN_LOCATION_OBJECT = ReturnLocation(
    return_to="test-return-to",
    return_to_block_id="test-return-to-block-id",
    return_to_answer_id="test-return-to-answer-id",
    return_to_list_item_id="return-to-list-item-id",
)


def test_return_location_to_dict():
    assert TEST_RETURN_LOCATION_OBJECT.to_dict() == {
        "return_to": "test-return-to",
        "return_to_block_id": "test-return-to-block-id",
        "return_to_answer_id": "test-return-to-answer-id",
        "return_to_list_item_id": "return-to-list-item-id",
    }


def test_return_location_to_dict_with_anchor_return_to_answer_id():
    assert TEST_RETURN_LOCATION_OBJECT.to_dict(answer_id_is_anchor=True) == {
        "return_to": "test-return-to",
        "return_to_block_id": "test-return-to-block-id",
        "_anchor": "test-return-to-answer-id",
        "return_to_list_item_id": "return-to-list-item-id",
    }
