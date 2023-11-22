from app.questionnaire.location import Location
from app.questionnaire.return_location import ReturnLocation
from app.views.contexts.summary.block import Block


def test_create_block(mocker):
    # Given
    block_schema = {
        "id": "block_id",
        "title": "A section title",
        "number": "1",
        "question": {"id": "mock_question_schema"},
    }
    location = Location(section_id="a-section")

    return_location = ReturnLocation(return_to="final-summary")

    question = mocker.MagicMock()
    question.serialize = mocker.MagicMock(return_value="A Question")

    # When
    mocker.patch(
        "app.views.contexts.summary.block.Question",
        return_value=question,
    )
    block = Block(
        block_schema,
        data_stores=mocker.MagicMock(),
        schema=mocker.MagicMock(),
        location=location,
        return_location=return_location,
        language="en",
    )

    # Then
    assert block.id == "block_id"
    assert block.title == "A section title"
    assert block.number == "1"
    assert block.question == "A Question"
