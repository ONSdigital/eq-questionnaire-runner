import pytest

from app.questionnaire.rules.operations import DateOffset


def test_string_to_datetime(operation_helper):
    offset = DateOffset(days=-1 * 7, day_of_week="MONDAY")
    offset_by_full_weeks = True
    actual = operation_helper.string_to_datetime(
        "2021-09-26", offset, offset_by_full_weeks
    )
    assert str(actual) == "2021-09-13"


@pytest.mark.parametrize(
    "answer_id, value, expected",
    [
        (
            "mandatory-radio-answer",
            "{business_name} (piped)",
            "ESSENTIAL SERVICES LTD (piped)",
        ),
        ("mandatory-radio-answer", "Google LTD", "Google LTD"),
    ],
)
def test_get_option_label_from_value(
    operation_helper, answer_id, value, expected, mocker
):
    mocker.patch(
        "app.questionnaire.placeholder_parser.PlaceholderParser._get_block_ids_for_calculated_summary_dependencies",
        return_value=[],
    )

    actual = operation_helper.get_option_label_from_value(value, answer_id)

    assert actual == expected
