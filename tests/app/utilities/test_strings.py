import pytest

from app.utilities import strings


@pytest.mark.parametrize(
    "input_str, bytes_str",
    (
        ("abc", b"abc"),
        (b"def", b"def"),
        (None, None),
        ("", b""),
    ),
)
def test_to_bytes(input_str, bytes_str):
    assert strings.to_bytes(input_str) == bytes_str


@pytest.mark.parametrize(
    "input_str, bytes_str",
    (
        ("hij", "hij"),
        (b"klm", "klm"),
        (None, None),
        (b"", ""),
    ),
)
def test_to_str(input_str, bytes_str):
    assert strings.to_str(input_str) == bytes_str


@pytest.mark.parametrize(
    "input_str, expected_result",
    (
        ("CalculatedSummary", "calculated-summary"),
        ("GrandCalculatedSummary", "grand-calculated-summary"),
        ("Block", "block"),
    ),
)
def test_pascal_case_to_hyphenated_lowercase(input_str, expected_result):
    assert strings.pascal_case_to_hyphenated_lowercase(input_str) == expected_result
