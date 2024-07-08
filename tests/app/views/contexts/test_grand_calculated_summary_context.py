import pytest

from app.data_models import CompletionStatus
from app.data_models.data_stores import DataStores
from app.data_models.progress_store import ProgressStore
from app.questionnaire import Location
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.return_location import ReturnLocation
from app.questionnaire.routing_path import RoutingPath
from app.views.contexts.grand_calculated_summary_context import (
    GrandCalculatedSummaryContext,
)
from tests.app.views.contexts import assert_summary_context


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "block_id, title, value, return_to_answer_id",
    (
        (
            "distance-grand-calculated-summary",
            "We calculate the grand total weekly distance travelled to be 100 mi. Is this correct?",
            "100 mi",
            "distance-calculated-summary-1",
        ),
        (
            "number-grand-calculated-summary",
            "We calculate the grand total journeys per week to be 10. Is this correct?",
            "10",
            "number-calculated-summary-1",
        ),
    ),
)
# pylint: disable=too-many-locals
def test_build_view_context_for_grand_calculated_summary(
    block_id,
    title,
    value,
    test_grand_calculated_summary_schema,
    test_grand_calculated_summary_answers,
    mocker,
    return_to_answer_id,
):
    mocker.patch(
        "app.jinja_filters.flask_babel.get_locale",
        mocker.MagicMock(return_value="en_GB"),
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

    current_location = Location(section_id="default-section", block_id=block_id)
    data_stores = DataStores(
        answer_store=test_grand_calculated_summary_answers,
        progress_store=ProgressStore(
            progress=[
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
    )
    block = test_grand_calculated_summary_schema.get_block(block_id)
    language = "en"

    placeholder_renderer = PlaceholderRenderer(
        language=language,
        data_stores=data_stores,
        schema=test_grand_calculated_summary_schema,
        location=current_location,
    )

    rendered_block = placeholder_renderer.render(
        data_to_render=block, list_item_id=current_location.list_item_id
    )

    grand_calculated_summary_context = GrandCalculatedSummaryContext(
        language=language,
        schema=test_grand_calculated_summary_schema,
        data_stores=data_stores,
        routing_path=RoutingPath(section_id="default-section", block_ids=block_ids),
        current_location=current_location,
        return_location=ReturnLocation(),
        rendered_block=rendered_block,
    )

    context = grand_calculated_summary_context.build_view_context()

    assert "summary" in context
    assert_summary_context(context, "calculated_summary")
    assert len(context["summary"]) == 6
    context_summary = context["summary"]
    assert context_summary.get("title") == title

    assert "calculated_question" in context_summary
    assert context_summary["calculated_question"]["answers"][0]["value"] == value

    calculated_summary_change_link = context_summary["sections"][0]["groups"][0][
        "blocks"
    ][0]["calculated_summary"]["answers"][0]["link"]
    assert "return_to=grand-calculated-summary" in calculated_summary_change_link
    assert (
        f"return_to_answer_id={return_to_answer_id}" in calculated_summary_change_link
    )
    assert f"return_to_block_id={block_id}" in calculated_summary_change_link
