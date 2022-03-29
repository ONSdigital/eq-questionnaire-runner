import pytest

from app.questionnaire.location import InvalidLocationException
from app.views.handlers.block_factory import get_block_handler


def test_get_handler_invalid_block(mocker):
    schema = mocker.Mock()
    schema.get_block = mocker.Mock(return_value=None)
    with pytest.raises(InvalidLocationException):
        get_block_handler(
            schema=schema,
            block_id="invalid-block-id",
            list_item_id=None,
            list_name="",
            questionnaire_store=None,
            language=None,
        )


@pytest.mark.parametrize(
    "block_type, is_block_in_repeating_section, list_name, exc",
    (
        ("MadeUpType", False, "", ValueError),
        ("Question", True, "", InvalidLocationException),
        ("Question", True, "people", InvalidLocationException),
    ),
)
def test_get_handler_invalid_block_raises_value_error(
    block_type, is_block_in_repeating_section, list_name, exc, mocker
):
    schema = mocker.Mock()
    schema.get_block = mocker.Mock(
        return_value={"id": "some-block", "type": block_type}
    )
    schema.is_block_in_repeating_section = mocker.Mock(
        return_value=is_block_in_repeating_section
    )

    with pytest.raises(exc):
        get_block_handler(
            schema=schema,
            block_id="some-block",
            list_item_id=None,
            list_name=list_name,
            questionnaire_store=None,
            language=None,
        )
