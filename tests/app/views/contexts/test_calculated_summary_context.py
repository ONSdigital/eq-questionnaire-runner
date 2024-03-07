import pytest

from app.data_models import AnswerStore, ListStore
from app.data_models.data_stores import DataStores
from app.questionnaire import Location
from app.questionnaire.return_location import ReturnLocation
from app.questionnaire.routing_path import RoutingPath
from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from tests.app.views.contexts import assert_summary_context


# pylint: disable=too-many-locals
@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "block_id, locale, language, title, value, total_blocks, return_to_answer_id, skip_fourth",
    (
        (
            "currency-total-playback",
            "en_GB",
            "en",
            "We calculate the total of currency values entered to be £27.00. Is this correct?",
            "£27.00",
            5,
            "first-number-answer",
            False,
        ),
        (
            "currency-total-playback",
            "en_GB",
            "en",
            "We calculate the total of currency values entered to be £12.00. Is this correct?",
            "£12.00",
            3,
            "first-number-answer",
            True,
        ),
        (
            "unit-total-playback",
            "cy",
            "cy",
            "We calculate the total of unit values entered to be 9 cm. Is this correct?",
            "9 cm",
            2,
            "second-number-answer-unit-total",
            False,
        ),
        (
            "percentage-total-playback",
            "en_GB",
            "en",
            "We calculate the total of percentage values entered to be 20%. Is this correct?",
            "20%",
            2,
            "fifth-percent-answer",
            False,
        ),
        (
            "number-total-playback",
            "cy",
            "cy",
            "We calculate the total of number values entered to be 22. Is this correct?",
            "22",
            2,
            "fifth-number-answer",
            False,
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
    test_calculated_summary_answers_skipped_fourth,
    mocker,
    return_to_answer_id,
    skip_fourth,
):
    mocker.patch(
        "app.jinja_filters.flask_babel.get_locale",
        mocker.MagicMock(return_value=locale),
    )

    block_ids = (
        [
            "first-number-block",
            "second-number-block",
            "third-number-block",
            "third-and-a-half-number-block",
            "skip-fourth-block",
            "fifth-number-block",
            "sixth-number-block",
        ]
        if skip_fourth
        else [
            "first-number-block",
            "second-number-block",
            "third-number-block",
            "third-and-a-half-number-block",
            "skip-fourth-block",
            "fourth-number-block",
            "fourth-and-a-half-number-block",
            "fifth-number-block",
            "sixth-number-block",
        ]
    )

    calculated_summary_context = CalculatedSummaryContext(
        language=language,
        schema=test_calculated_summary_schema,
        data_stores=DataStores(
            answer_store=(
                test_calculated_summary_answers_skipped_fourth
                if skip_fourth
                else test_calculated_summary_answers
            )
        ),
        routing_path=RoutingPath(section_id="default-section", block_ids=block_ids),
        current_location=Location(section_id="default-section", block_id=block_id),
        return_location=ReturnLocation(return_to_answer_id=return_to_answer_id),
    )

    context = calculated_summary_context.build_view_context()

    assert "summary" in context
    assert_summary_context(context)
    assert len(context["summary"]) == 6
    context_summary = context["summary"]
    assert "title" in context_summary
    assert context_summary["title"] == title

    assert "calculated_question" in context_summary
    assert len(context_summary["sections"][0]["groups"][0]["blocks"]) == total_blocks
    assert (
        context_summary["calculated_question"]["title"]
        == "Grand total of previous values"
    )
    assert context_summary["calculated_question"]["answers"][0]["value"] == value

    answer_change_link = context_summary["sections"][0]["groups"][0]["blocks"][0][
        "question"
    ]["answers"][0]["link"]
    assert "return_to=calculated-summary" in answer_change_link
    assert f"return_to_answer_id={return_to_answer_id}" in answer_change_link
    assert f"return_to_block_id={block_id}" in answer_change_link


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "block_id, return_to_answer_id, return_to, return_to_block_id",
    (
        (
            "distance-calculated-summary-1",
            "q1-a1",
            "grand-calculated-summary",
            "distance-grand-calculated-summary",
        ),
        (
            "number-calculated-summary-1",
            "q1-a2",
            "grand-calculated-summary",
            "number-grand-calculated-summary",
        ),
        (
            "distance-calculated-summary-2",
            "q3-a1",
            "grand-calculated-summary",
            "distance-grand-calculated-summary",
        ),
        (
            "number-calculated-summary-2",
            "q3-a2",
            "grand-calculated-summary",
            "number-grand-calculated-summary",
        ),
    ),
)
def test_build_view_context_for_return_to_calculated_summary(
    test_grand_calculated_summary_schema,
    test_grand_calculated_summary_answers,
    mocker,
    block_id,
    return_to_answer_id,
    return_to,
    return_to_block_id,
):
    """
    Tests the change answer links for a calculated summary that has been reached by a change link on a grand calculated summary
    """
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

    calculated_summary_context = CalculatedSummaryContext(
        language="en",
        schema=test_grand_calculated_summary_schema,
        data_stores=DataStores(answer_store=test_grand_calculated_summary_answers),
        routing_path=RoutingPath(section_id="default-section", block_ids=block_ids),
        current_location=Location(section_id="default-section", block_id=block_id),
        return_location=ReturnLocation(
            return_to=return_to, return_to_block_id=return_to_block_id
        ),
    )

    context = calculated_summary_context.build_view_context()
    assert "summary" in context
    assert_summary_context(context)
    context_summary = context["summary"]

    answer_change_link = context_summary["sections"][0]["groups"][0]["blocks"][0][
        "question"
    ]["answers"][0]["link"]
    assert f"return_to=calculated-summary,{return_to}" in answer_change_link
    assert f"return_to_answer_id={return_to_answer_id}" in answer_change_link
    assert f"return_to_block_id={block_id},{return_to_block_id}" in answer_change_link


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "block_id,expected_answer_ids,expected_block_ids",
    (
        (
            "calculated-summary-spending",
            [
                "cost-of-shopping-CHKtQS",
                "cost-of-shopping-laFWcs",
                "cost-of-other-CHKtQS",
                "cost-of-other-laFWcs",
                "extra-static-answer",
            ],
            ["dynamic-answer", "extra-spending-block"],
        ),
        (
            "calculated-summary-visits",
            [
                "days-a-week-CHKtQS",
                "days-a-week-laFWcs",
            ],
            ["dynamic-answer"],
        ),
    ),
)
def test_build_view_context_for_calculated_summary_with_dynamic_answers(
    test_calculated_summary_repeating_and_static_answers_schema,
    mocker,
    block_id,
    expected_answer_ids,
    expected_block_ids,
):
    """
    Tests that when different dynamic answers for the same list are used in different calculated summaries
    that the calculated summary context filters the answers to keep correctly.
    """
    mocker.patch(
        "app.jinja_filters.flask_babel.get_locale",
        mocker.MagicMock(return_value="en_GB"),
    )

    block_ids = [
        "any-supermarket",
        "list-collector",
        "dynamic-answer",
        "extra-spending-block",
    ]

    calculated_summary_context = CalculatedSummaryContext(
        language="en",
        schema=test_calculated_summary_repeating_and_static_answers_schema,
        data_stores=DataStores(
            list_store=ListStore(
                [{"items": ["CHKtQS", "laFWcs"], "name": "supermarkets"}]
            )
        ),
        routing_path=RoutingPath(section_id="section-1", block_ids=block_ids),
        current_location=Location(section_id="section-1", block_id=block_id),
        return_location=ReturnLocation(),
    )

    context = calculated_summary_context.build_view_context()
    assert "summary" in context
    assert_summary_context(context)
    context_summary = context["summary"]
    calculation_blocks = context_summary["sections"][0]["groups"][0]["blocks"]

    block_ids = [block["id"] for block in calculation_blocks]
    assert block_ids == expected_block_ids

    answers_to_keep = calculation_blocks[0]["question"]["answers"]
    answer_ids = [answer["id"] for answer in answers_to_keep]
    assert answer_ids == expected_answer_ids

    # blocks with dynamic answers show each answer suffixed with the list item id, so the anchor needs to also include it
    assert all(
        answer["link"].endswith(
            f"return_to=calculated-summary&return_to_answer_id={answer['id']}&return_to_block_id={block_id}#{answer['id']}"
        )
        for answer in answers_to_keep
    )


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "block_id,expected_answer_ids,expected_answer_labels,expected_block_ids,anchors",
    (
        (
            "calculated-summary-spending",
            [
                "answer-car",
                "transport-cost-CHKtQS",
                "transport-additional-cost-CHKtQS",
                "transport-cost-laFWcs",
                "transport-additional-cost-laFWcs",
            ],
            [
                "Monthly expenditure travelling by car",
                "Monthly season ticket expenditure for travel by Train",
                "Additional monthly expenditure for travel by Train",
                "Monthly season ticket expenditure for travel by Bus",
                "Additional monthly expenditure for travel by Bus",
            ],
            [
                "block-car",
                "transport-repeating-block-1-CHKtQS",
                "transport-repeating-block-1-laFWcs",
            ],
            [
                "answer-car",
                "transport-cost",
                "transport-additional-cost",
                "transport-cost",
                "transport-additional-cost",
            ],
        ),
        (
            "calculated-summary-count",
            ["transport-count-CHKtQS", "transport-count-laFWcs"],
            ["Monthly journeys by Train", "Monthly journeys by Bus"],
            [
                "transport-repeating-block-2-CHKtQS",
                "transport-repeating-block-2-laFWcs",
            ],
            ["transport-count", "transport-count"],
        ),
    ),
)
def test_build_view_context_for_calculated_summary_with_answers_from_repeating_blocks(
    test_calculated_summary_repeating_blocks,
    mocker,
    block_id,
    expected_answer_ids,
    expected_answer_labels,
    expected_block_ids,
    anchors,
):
    """
    Tests that when different dynamic answers for the same list are used in different calculated summaries
    that the calculated summary context filters the answers to keep correctly.
    """
    mocker.patch(
        "app.jinja_filters.flask_babel.get_locale",
        mocker.MagicMock(return_value="en_GB"),
    )

    block_ids = ["block-car", "list-collector"]

    calculated_summary_context = CalculatedSummaryContext(
        language="en",
        schema=test_calculated_summary_repeating_blocks,
        data_stores=DataStores(
            answer_store=AnswerStore(
                [
                    {
                        "answer_id": "transport-name",
                        "value": "Train",
                        "list_item_id": "CHKtQS",
                    },
                    {
                        "answer_id": "transport-name",
                        "value": "Bus",
                        "list_item_id": "laFWcs",
                    },
                ]
            ),
            list_store=ListStore(
                [{"items": ["CHKtQS", "laFWcs"], "name": "transport"}]
            ),
        ),
        routing_path=RoutingPath(section_id="section-1", block_ids=block_ids),
        current_location=Location(section_id="section-1", block_id=block_id),
        return_location=ReturnLocation(),
    )

    context = calculated_summary_context.build_view_context()
    assert "summary" in context
    assert_summary_context(context)
    context_summary = context["summary"]
    calculation_blocks = context_summary["sections"][0]["groups"][0]["blocks"]

    block_ids = [block["id"] for block in calculation_blocks]
    assert block_ids == expected_block_ids

    questions = [block["question"] for block in calculation_blocks]
    answers = [answer for question in questions for answer in question["answers"]]
    answer_ids = [answer["id"] for answer in answers]
    assert answer_ids == expected_answer_ids

    answer_labels = [answer["label"] for answer in answers]
    assert answer_labels == expected_answer_labels

    # on summary pages, repeating block answer ids are suffixed with list item ids,
    # but the anchor on the change links needs to not have them, because the repeating block itself doesn't do that
    assert all(
        answer["link"].endswith(
            f"return_to=calculated-summary&return_to_answer_id={answer['id']}&return_to_block_id={block_id}#{anchor}"
        )
        for anchor, answer in zip(anchors, answers)
    )
