import pytest

from app.questionnaire.location import Location
from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from tests.app.views.contexts import assert_summary_context


# pylint: disable=too-many-locals
@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "block_id, locale, language, title, value, total_blocks, return_to_answer_id",
    (
        (
            "currency-total-playback-with-fourth",
            "en_GB",
            "en",
            "We calculate the total of currency values entered to be £27.00. Is this correct? (With Fourth)",
            "£27.00",
            5,
            "first-number-answer",
        ),
        (
            "currency-total-playback-skipped-fourth",
            "en_GB",
            "en",
            "We calculate the total of currency values entered to be £12.00. Is this correct? (Skipped Fourth)",
            "£12.00",
            3,
            "first-number-answer",
        ),
        (
            "unit-total-playback",
            "cy",
            "cy",
            "We calculate the total of unit values entered to be 9 cm. Is this correct?",
            "9 cm",
            2,
            "second-number-answer-unit-total",
        ),
        (
            "percentage-total-playback",
            "en_GB",
            "en",
            "We calculate the total of percentage values entered to be 20%. Is this correct?",
            "20%",
            2,
            "fifth-percent-answer",
        ),
        (
            "number-total-playback",
            "cy",
            "cy",
            "We calculate the total of number values entered to be 22. Is this correct?",
            "22",
            2,
            "fifth-number-answer",
        ),
    ),
)
def test_build_view_context_for_currency_calculated_summary(
    block_id,
    locale,
    language,
    title,
    value,
    total_blocks,
    test_calculated_summary_schema,
    test_calculated_summary_answers,
    list_store,
    progress_store,
    mocker,
    return_to_answer_id,
):
    mocker.patch(
        "app.jinja_filters.flask_babel.get_locale",
        mocker.MagicMock(return_value=locale),
    )

    current_location = Location(section_id="default-section", block_id=block_id)

    calculated_summary_context = CalculatedSummaryContext(
        language,
        test_calculated_summary_schema,
        test_calculated_summary_answers,
        list_store,
        progress_store,
        metadata={},
        response_metadata={},
    )

    context = calculated_summary_context.build_view_context_for_calculated_summary(
        current_location
    )

    assert "summary" in context
    assert_summary_context(context)
    assert len(context["summary"]) == 7
    context_summary = context["summary"]
    assert "title" in context_summary
    assert context_summary["title"] == title

    assert "calculated_question" in context_summary
    assert len(context_summary["groups"][0]["blocks"]) == total_blocks
    assert (
        context_summary["calculated_question"]["title"]
        == "Grand total of previous values"
    )
    assert context_summary["calculated_question"]["answers"][0]["value"] == value

    answer_change_link = context_summary["groups"][0]["blocks"][0]["question"][
        "answers"
    ][0]["link"]
    assert "return_to=calculated-summary" in answer_change_link
    assert f"return_to_answer_id={return_to_answer_id}" in answer_change_link
    assert f"return_to_block_id={block_id}" in answer_change_link
