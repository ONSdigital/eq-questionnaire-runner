import pytest

from app.helpers.uuid_helper import is_valid_uuid
from app.libs.utils import convert_tx_id, escape_value


def test_convert_tx_id():
    tx_id_to_convert = "bc26d5ef-8475-4710-ac82-753a0a150708"

    assert is_valid_uuid(tx_id_to_convert)
    assert "bc26-d5ef-8475-4710" == convert_tx_id(tx_id_to_convert)


HTML_CONTENT = '"><b>some html</b>'
ESCAPED_CONTENT = "&#34;&gt;&lt;b&gt;some html&lt;/b&gt;"


@pytest.mark.parametrize(
    "value_to_escape, escaped_value",
    [
        (HTML_CONTENT, ESCAPED_CONTENT),
        ([HTML_CONTENT, 1, HTML_CONTENT], [ESCAPED_CONTENT, 1, ESCAPED_CONTENT]),
        ({"key_1": HTML_CONTENT, "key_2": 1}, {"key_1": ESCAPED_CONTENT, "key_2": 1}),
        (1, 1),
        (None, None),
    ],
)
def test_escape_value(value_to_escape, escaped_value):
    assert escape_value(value_to_escape) == escaped_value
