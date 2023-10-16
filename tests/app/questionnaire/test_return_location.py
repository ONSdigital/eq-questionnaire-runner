import pytest

from app.questionnaire.location import SectionKey
from app.questionnaire.return_location import ReturnLocation


@pytest.mark.usefixtures("app")
def test_location_url():
    return_location = ReturnLocation(
        return_to="test-return-to",
        return_to_block_id="test-return-to-block-id",
        return_to_answer_id="test-return-to-answer-id",  # TODO: This can be an anchor, so make sure to check for it when unpacking in the to_dict function
        return_to_list_name="test-return-to-list-name",
        return_to_list_item_id="return-to-list-item-id",
    # anchor: # TODO: Check if this can live in the class, or whether it's
    )

    assert return_location.to_dict() == {
        "return_to": "test-return-to",
        "return_to_block_id": "test-return-to-block-id",
        "return_to_answer_id": "test-return-to-answer-id",
        "return_to_list_name": "test-return-to-list-name",
        "return_to_list_item_id": "return-to-list-item-id",
    }
