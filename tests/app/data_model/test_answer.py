import pytest

from app.data_models.answer import escape_answer_value
from app.data_models.answer_store import Answer

HTML_CONTENT = '"><b>some html</b>'
ESCAPED_CONTENT = "&#34;&gt;&lt;b&gt;some html&lt;/b&gt;"


def test_from_dict():
    test_answer = {"answer_id": "test1", "value": "avalue", "list_item_id": "123321"}

    expected_answer = Answer(answer_id="test1", value="avalue", list_item_id="123321")

    assert Answer.from_dict(test_answer) == expected_answer


@pytest.mark.parametrize(
    "value_to_escape, escaped_value",
    [
        (HTML_CONTENT, ESCAPED_CONTENT),
        ([HTML_CONTENT, "some value"], [ESCAPED_CONTENT, "some value"]),
        ({"key_1": HTML_CONTENT, "key_2": 1}, {"key_1": ESCAPED_CONTENT, "key_2": 1}),
        (1, 1),
        (None, None),
    ],
)
def test_escape_value(value_to_escape, escaped_value):
    assert escape_answer_value(value_to_escape) == escaped_value
