import pytest

from app.data_models.progress_store import CompletionStatus, ProgressStore
from app.questionnaire import Location
from app.questionnaire.routing_path import RoutingPath
from app.views.contexts.grand_calculated_summary_context import (
    GrandCalculatedSummaryContext,
)
from tests.app.views.contexts import assert_summary_context


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "block_id, locale, language, title, value, total_blocks, return_to_answer_id",
    (
        (
            "distance-grand-calculated-summary",
            "en_GB",
            "en",
            "We calculate the grand total weekly distance travelled to be 100 mi. Is this correct?",
            "100 mi",
            2,
            "distance-calculated-summary-1",
        ),
        (
            "number-grand-calculated-summary",
            "en_GB",
            "en",
            "We calculate the grand total journeys per week to be 10. Is this correct?",
            "10",
            2,
            "number-calculated-summary-1",
        ),
    ),
)
def test_build_view_context_for_grand_calculated_summary(
    block_id,
    locale,
    language,
    title,
    value,
    total_blocks,
    test_grand_calculated_summary_schema,
    test_grand_calculated_summary_answers,
    list_store,
    mocker,
    return_to_answer_id,
):
    mocker.patch(
        "app.jinja_filters.flask_babel.get_locale",
        mocker.MagicMock(return_value=locale),
    )

    block_ids = [
        "first-number-block",
        "second-number-block",
        "distance-calculated-summary-1",
        "number-calculated-summary-1",
        "third-number-block",
        "fourth-number-block",
        "distance-calculated-summary-2",
        "number-calculated-summary-2",
    ]

    grand_calculated_summary_context = GrandCalculatedSummaryContext(
        language=language,
        schema=test_grand_calculated_summary_schema,
        answer_store=test_grand_calculated_summary_answers,
        list_store=list_store,
        progress_store=ProgressStore(
            in_progress_sections=[
                {
                    "section_id": "section-1",
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": [
                        "first-number-block",
                        "second-number-block",
                        "distance-calculated-summary-1",
                        "number-calculated-summary-1",
                    ],
                },
                {
                    "section_id": "section-2",
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": [
                        "third-number-block",
                        "fourth-number-block",
                        "distance-calculated-summary-2",
                        "number-calculated-summary-2",
                    ],
                },
            ]
        ),
        metadata=None,
        response_metadata={},
        routing_path=RoutingPath(section_id="default-section", block_ids=block_ids),
        current_location=Location(section_id="default-section", block_id=block_id),
        return_to=None,
        return_to_block_id=None,
    )

    context = (
        grand_calculated_summary_context.build_view_context_for_grand_calculated_summary()
    )

    assert "summary" in context
    assert_summary_context(context, "calculated_summary")
    assert len(context["summary"]) == 6
    context_summary = context["summary"]
    assert "title" in context_summary
    assert context_summary["title"] == title

    assert "calculated_question" in context_summary
    assert len(context_summary["groups"][0]["blocks"]) == total_blocks
    assert context_summary["calculated_question"]["answers"][0]["value"] == value

    answer_change_link = context_summary["groups"][0]["blocks"][0][
        "calculated_summary"
    ]["answers"][0]["link"]
    assert "return_to=grand-calculated-summary" in answer_change_link
    assert f"return_to_answer_id={return_to_answer_id}" in answer_change_link
    assert f"return_to_block_id={block_id}" in answer_change_link
