from app.data_models.answer_store import Answer


def test_from_dict():
    test_answer = {"answer_id": "test1", "value": "avalue", "list_item_id": "123321"}

    expected_answer = Answer(answer_id="test1", value="avalue", list_item_id="123321")

    assert Answer.from_dict(test_answer) == expected_answer
