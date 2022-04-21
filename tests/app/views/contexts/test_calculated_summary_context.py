import pytest

from app.questionnaire.location import Location
from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from tests.app.views.contexts import assert_summary_context


# pylint: disable=too-many-locals
@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "block_id, locale, language, title, value, total_blocks",
    (
        (
            "currency-total-playback-with-fourth",
            "en_GB",
            "en",
            "We calculate the total of currency values entered to be £27.00. Is this correct? (With Fourth)",
            "£27.00",
            5,
        ),
        (
            "currency-total-playback-skipped-fourth",
            "en_GB",
            "en",
            "We calculate the total of currency values entered to be £12.00. Is this correct? (Skipped Fourth)",
            "£12.00",
            3,
        ),
        (
            "unit-total-playback",
            "cy",
            "cy",
            "We calculate the total of unit values entered to be 9 cm. Is this correct?",
            "9 cm",
            2,
        ),
        (
            "percentage-total-playback",
            "en_GB",
            "en",
            "We calculate the total of percentage values entered to be 20%. Is this correct?",
            "20%",
            2,
        ),
        (
            "number-total-playback",
            "cy",
            "cy",
            "We calculate the total of number values entered to be 22. Is this correct?",
            "22",
            2,
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
    assert len(context["summary"]) == 6
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
    assert "return_to=final-summary" in answer_change_link


@pytest.mark.parametrize(
    "has_section_summary",
    ([True, False]),
)
@pytest.mark.parametrize(
    "is_hub_enabled",
    ([True, False]),
)
def test_get_return_to(
    has_section_summary,
    is_hub_enabled,
    mocker,
):
    schema = mocker.MagicMock()
    schema.is_flow_hub = is_hub_enabled
    schema.get_summary_for_section = mocker.Mock(return_value=has_section_summary)

    calculated_summary_context = CalculatedSummaryContext(
        "en",
        schema,
        answer_store=mocker.MagicMock(),
        list_store=mocker.MagicMock(),
        progress_store=mocker.MagicMock(),
        metadata={},
        response_metadata={},
    )

    return_to = calculated_summary_context.get_return_to("some-section")
    if has_section_summary:
        assert return_to == "section-summary"
    elif not is_hub_enabled:
        assert return_to == "final-summary"
    else:
        assert return_to is None
