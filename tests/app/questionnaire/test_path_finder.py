import pytest

from app.data_models import ListStore
from app.data_models.answer_store import Answer, AnswerStore
from app.data_models.progress_store import CompletionStatus, ProgressStore
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.routing_path import RoutingPath
from app.utilities.schema import load_schema_from_name


def test_simple_path(answer_store, list_store):
    schema = load_schema_from_name("test_textfield")
    progress_store = ProgressStore(
        [
            {
                "section_id": "default-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["name-block"],
            }
        ]
    )
    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})

    section_id = schema.get_section_id_for_block_id("name-block")
    routing_path = path_finder.routing_path(section_id=section_id)

    assumed_routing_path = RoutingPath(["name-block"], section_id="default-section")

    assert routing_path == assumed_routing_path


def test_introduction_in_path_when_in_schema(answer_store, list_store, progress_store):
    schema = load_schema_from_name("test_introduction")
    current_section = schema.get_section("introduction-section")

    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})

    routing_path = path_finder.routing_path(section_id=current_section["id"])
    assert "introduction" in routing_path


def test_introduction_not_in_path_when_not_in_schema(
    answer_store, list_store, progress_store, mocker
):
    schema = load_schema_from_name("test_checkbox")
    current_section = schema.get_section("default-section")
    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})

    mocker.patch("app.questionnaire.when_rules.evaluate_when_rules", return_value=False)
    routing_path = path_finder.routing_path(section_id=current_section["id"])

    assert "introduction" not in routing_path


@pytest.mark.parametrize(
    "schema",
    (
        "test_new_routing_number_equals",
        "test_routing_number_equals",
    ),
)
def test_routing_path_with_conditional_path(schema, answer_store, list_store):
    schema = load_schema_from_name(schema)
    section_id = schema.get_section_id_for_block_id("number-question")
    expected_path = RoutingPath(
        ["number-question", "correct-answer"],
        section_id="default-section",
    )

    answer = Answer(answer_id="answer", value=123)
    answer_store.add_or_update(answer)
    progress_store = ProgressStore(
        [
            {
                "section_id": "default-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["number-question"],
            }
        ]
    )
    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})

    routing_path = path_finder.routing_path(section_id=section_id)

    assert routing_path == expected_path


def test_new_routing_basic_and_conditional_path(
    answer_store, list_store, progress_store
):
    # Given
    schema = load_schema_from_name("test_new_routing_number_equals")
    section_id = schema.get_section_id_for_block_id("number-question")
    expected_path = RoutingPath(
        ["number-question", "correct-answer"],
        section_id="default-section",
    )

    answer_1 = Answer(answer_id="answer", value=123)

    answer_store.add_or_update(answer_1)

    # When
    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})
    routing_path = path_finder.routing_path(section_id=section_id)

    # Then
    assert routing_path == expected_path


def test_routing_path_with_complete_introduction(answer_store, list_store):
    schema = load_schema_from_name("test_introduction")
    section_id = schema.get_section_id_for_block_id("introduction")
    progress_store = ProgressStore(
        [
            {
                "section_id": "introduction-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["introduction"],
            }
        ]
    )
    expected_routing_path = RoutingPath(
        ["introduction", "general-business-information-completed"],
        section_id="introduction-section",
    )

    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})
    routing_path = path_finder.routing_path(section_id=section_id)

    assert routing_path == expected_routing_path


def test_routing_path(answer_store, list_store):
    schema = load_schema_from_name("test_submit_with_summary")
    section_id = schema.get_section_id_for_block_id("dessert")
    expected_path = RoutingPath(
        ["radio", "dessert", "dessert-confirmation", "numbers"],
        section_id="default-section",
    )

    progress_store = ProgressStore(
        [
            {
                "section_id": "default-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": [
                    "radio",
                    "dessert",
                    "dessert-confirmation",
                    "numbers",
                ],
            }
        ]
    )
    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})
    routing_path = path_finder.routing_path(section_id=section_id)

    assert routing_path == expected_path


def test_routing_path_with_repeating_sections(answer_store, list_store):
    schema = load_schema_from_name("test_repeating_sections_with_hub_and_spoke")

    progress_store = ProgressStore(
        [
            {
                "section_id": "section",
                "status": CompletionStatus.COMPLETED,
                "block_ids": [
                    "primary-person-list-collector",
                    "list-collector",
                    "next-interstitial",
                    "another-list-collector-block",
                ],
            }
        ]
    )
    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})

    repeating_section_id = "personal-details-section"
    routing_path = path_finder.routing_path(
        section_id=repeating_section_id, list_item_id="abc123"
    )

    expected_path = RoutingPath(
        ["proxy", "date-of-birth", "confirm-dob", "sex"],
        section_id="personal-details-section",
        list_name="people",
        list_item_id="abc123",
    )

    assert routing_path == expected_path


def test_routing_path_empty_routing_rules(answer_store, list_store):
    schema = load_schema_from_name("test_checkbox")
    section_id = schema.get_section_id_for_block_id("mandatory-checkbox")
    expected_path = RoutingPath(
        ["mandatory-checkbox", "non-mandatory-checkbox", "single-checkbox"],
        section_id="default-section",
    )

    answer_1 = Answer(answer_id="mandatory-checkbox-answer", value="Cheese")
    answer_2 = Answer(answer_id="non-mandatory-checkbox-answer", value="deep pan")
    answer_3 = Answer(answer_id="single-checkbox-answer", value="Estimate")

    answer_store.add_or_update(answer_1)
    answer_store.add_or_update(answer_2)
    answer_store.add_or_update(answer_3)

    progress_store = ProgressStore(
        [
            {
                "section_id": "default-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["mandatory-checkbox"],
            }
        ]
    )

    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})
    routing_path = path_finder.routing_path(section_id=section_id)

    assert routing_path == expected_path


def test_routing_path_with_conditional_value_not_in_metadata(answer_store, list_store):
    schema = load_schema_from_name("test_metadata_routing")
    section_id = schema.get_section_id_for_block_id("block1")
    expected_path = RoutingPath(
        ["block1", "block2", "block3"], section_id="default-section"
    )

    progress_store = ProgressStore(
        [
            {
                "section_id": "default-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["block1"],
            }
        ]
    )

    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})
    routing_path = path_finder.routing_path(section_id=section_id)

    assert routing_path == expected_path


@pytest.mark.parametrize(
    "schema, expected_routing_path_ids",
    (
        ("test_new_skip_condition_block", ["do-you-want-to-skip"]),
        ("test_skip_condition_block", ["do-you-want-to-skip", "a-non-skipped-block"]),
    ),
)
def test_new_routing_path_should_skip_block(
    schema, expected_routing_path_ids, answer_store, list_store
):
    # Given
    schema = load_schema_from_name(schema)
    section_id = schema.get_section_id_for_block_id("should-skip")
    answer_store.add_or_update(
        Answer(answer_id="do-you-want-to-skip-answer", value="Yes")
    )

    progress_store = ProgressStore(
        [
            {
                "section_id": "introduction-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["do-you-want-to-skip"],
            }
        ]
    )

    # When
    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})
    routing_path = path_finder.routing_path(section_id=section_id)

    # Then
    expected_routing_path = RoutingPath(
        expected_routing_path_ids,
        section_id="default-section",
    )

    assert routing_path == expected_routing_path


@pytest.mark.parametrize(
    "schema",
    (
        "test_skip_condition_group",
        "test_new_skip_condition_group",
    ),
)
def test_routing_path_should_skip_group(schema, answer_store, list_store):
    # Given
    schema = load_schema_from_name(schema)

    section_id = schema.get_section_id_for_block_id("do-you-want-to-skip")
    answer_store.add_or_update(
        Answer(answer_id="do-you-want-to-skip-answer", value="Yes")
    )
    progress_store = ProgressStore(
        [
            {
                "section_id": "default-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["do-you-want-to-skip"],
            }
        ]
    )

    # When
    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})
    routing_path = path_finder.routing_path(section_id=section_id)

    # Then
    expected_routing_path = RoutingPath(
        ["do-you-want-to-skip"],
        section_id="default-section",
    )

    assert routing_path == expected_routing_path


@pytest.mark.parametrize(
    "schema",
    (
        "test_skip_condition_group",
        "test_new_skip_condition_group",
    ),
)
def test_routing_path_should_not_skip_group(schema, answer_store, list_store):
    # Given
    schema = load_schema_from_name(schema)

    section_id = schema.get_section_id_for_block_id("do-you-want-to-skip")
    answer_store.add_or_update(
        Answer(answer_id="do-you-want-to-skip-answer", value="No")
    )
    progress_store = ProgressStore(
        [
            {
                "section_id": "default-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["do-you-want-to-skip"],
            }
        ]
    )

    # When
    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})
    routing_path = path_finder.routing_path(section_id=section_id)

    # Then
    expected_routing_path = RoutingPath(
        ["do-you-want-to-skip", "should-skip"],
        section_id="default-section",
    )

    assert routing_path == expected_routing_path


def test_get_routing_path_when_first_block_in_group_skipped(
    answer_store, list_store, progress_store
):
    # Given
    schema = load_schema_from_name("test_skip_condition_group")
    answer_store.add_or_update(
        Answer(answer_id="do-you-want-to-skip-answer", value="Yes")
    )

    # When
    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})

    # Then
    expected_route = RoutingPath(
        section_id="default-section",
        block_ids=["do-you-want-to-skip"],
    )

    assert expected_route == path_finder.routing_path(section_id="default-section")


def test_build_path_with_group_routing(answer_store, list_store, progress_store):
    # Given i have answered the routing question
    schema = load_schema_from_name("test_new_routing_group")
    section_id = schema.get_section_id_for_block_id("group2-block")

    answer_store.add_or_update(Answer(answer_id="which-group-answer", value="group2"))

    # When i build the path
    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})
    path = path_finder.routing_path(section_id=section_id)

    # Then it should route me straight to Group2 and not Group1
    assert "group1-block" not in path
    assert "group2-block" in path


def test_remove_answer_and_block_if_routing_backwards(list_store):
    schema = load_schema_from_name("test_confirmation_question")
    section_id = schema.get_section_id_for_block_id("confirm-zero-employees-block")

    # All blocks completed
    progress_store = ProgressStore(
        [
            {
                "section_id": "default-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": [
                    "number-of-employees-total-block",
                    "confirm-zero-employees-block",
                ],
            }
        ]
    )

    number_of_employees_answer = Answer(answer_id="number-of-employees-total", value=0)
    confirm_zero_answer = Answer(
        answer_id="confirm-zero-employees-answer", value="No I need to change this"
    )
    answer_store = AnswerStore({})
    answer_store.add_or_update(number_of_employees_answer)
    answer_store.add_or_update(confirm_zero_answer)

    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})

    assert (
        len(
            path_finder.progress_store.get_completed_block_ids(
                section_id="default-section"
            )
        )
        == 2
    )
    assert len(path_finder.answer_store) == 2

    routing_path = path_finder.routing_path(section_id=section_id)

    expected_path = RoutingPath(
        [
            "number-of-employees-total-block",
            "confirm-zero-employees-block",
            "number-of-employees-total-block",
        ],
        section_id="default-section",
    )
    assert routing_path == expected_path

    assert path_finder.progress_store.get_completed_block_ids(
        section_id="default-section"
    ) == [progress_store.get_completed_block_ids(section_id="default-section")[0]]

    assert len(path_finder.answer_store) == 1
    assert not path_finder.answer_store.get_answer("confirm-zero-employees-answer")

    assert (
        progress_store.get_section_status(section_id="default-section")
        == CompletionStatus.IN_PROGRESS
    )


def test_new_remove_answer_and_block_if_routing_backwards(list_store):
    schema = load_schema_from_name("test_new_confirmation_question")
    section_id = schema.get_section_id_for_block_id("confirm-zero-employees-block")

    # All blocks completed
    progress_store = ProgressStore(
        [
            {
                "section_id": "default-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": [
                    "route-backwards-block",
                    "number-of-employees-total-block",
                    "confirm-zero-employees-block",
                ],
            }
        ]
    )

    answer_store = AnswerStore()
    route_backwards_answer = Answer(answer_id="route-backwards-answer", value="Yes")
    number_of_employees_answer = Answer(answer_id="number-of-employees-total", value=0)
    confirm_zero_answer = Answer(answer_id="confirm-zero-employees-answer", value="No")
    answer_store.add_or_update(route_backwards_answer)
    answer_store.add_or_update(number_of_employees_answer)
    answer_store.add_or_update(confirm_zero_answer)

    path_finder = PathFinder(schema, answer_store, list_store, progress_store, {}, {})

    assert (
        len(
            path_finder.progress_store.get_completed_block_ids(
                section_id="default-section"
            )
        )
        == 3
    )
    assert len(path_finder.answer_store) == 3

    routing_path = path_finder.routing_path(section_id=section_id)

    expected_path = RoutingPath(
        [
            "route-backwards-block",
            "number-of-employees-total-block",
            "confirm-zero-employees-block",
            "number-of-employees-total-block",
        ],
        section_id="default-section",
    )
    assert routing_path == expected_path
    assert path_finder.progress_store.get_completed_block_ids(
        section_id="default-section"
    ) == progress_store.get_completed_block_ids(section_id="default-section")

    assert len(path_finder.answer_store) == 2
    assert not path_finder.answer_store.get_answer("confirm-zero-employees-answer")
    assert (
        path_finder.progress_store.get_section_status(section_id="default-section")
        == CompletionStatus.IN_PROGRESS
    )


@pytest.mark.parametrize(
    "skip_age_answer, skip_confirmation_answer, section_id, expected_route",
    (
        (
            # Answering 'Yes' to the skip age question
            # means in skip-confirmation-section you will get a skip confirmation question
            "Yes",
            None,
            "skip-confirmation-section",
            ["security", "skip-confirmation"],
        ),
        (
            # Answering 'Yes' to the skip age question but not answering the skip-confirmation question
            # means in primary-person you will not be asked your age, but will be asked your name and why you didn't confirm skipping
            "Yes",
            None,
            "primary-person",
            ["name-block", "reason-no-confirmation"],
        ),
        (
            # Answering 'No' to the skip age question
            # means in skip-confirmation-section you will not get a skip confirmation question
            "No",
            None,
            "skip-confirmation-section",
            ["security"],
        ),
        (
            # Answering 'No' to the skip age question and not answering the skip-confirmation question
            # means in primary-person you will be asked your age, name and why you didn't confirm skipping
            "No",
            None,
            "primary-person",
            ["name-block", "age", "reason-no-confirmation"],
        ),
        (
            # Answering 'Yes' to the skip age question and the skip-confirmation question
            # means in primary-person you will be asked just your name
            "Yes",
            "Yes",
            "primary-person",
            ["name-block"],
        ),
        (
            # Answering 'Yes' to the skip age question and 'No' to the skip-confirmation question
            # means in primary-person you will only be asked your name and age
            "Yes",
            "No",
            "primary-person",
            ["name-block", "age"],
        ),
        (  # Answering 'Yes' to the skip age question and the skip-confirmation question, but then changing you answer for the skip age question to 'No'
            # means because confirmation is not longer on the path in primary-person you will be asked your age, name and why you didn't confirm skipping
            "No",
            "Yes",
            "primary-person",
            ["name-block", "age", "reason-no-confirmation"],
        ),
    ),
)
@pytest.mark.parametrize(
    "schema_name",
    (
        [
            "test_new_routing_and_skipping_section_dependencies",
            "test_routing_and_skipping_section_dependencies",
        ]
    ),
)
def test_routing_path_block_ids_dependent_on_other_sections_when_rules(
    list_store,
    skip_age_answer,
    skip_confirmation_answer,
    schema_name,
    section_id,
    expected_route,
    answer_store,
):
    # Given a schema which has when rules in a section which has dependencies on other sections answers
    schema = load_schema_from_name(schema_name)
    answer_store.add_or_update(
        Answer(answer_id="skip-age-answer", value=skip_age_answer)
    )

    progress = [
        {
            "section_id": "skip-section",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["skip-age"],
        }
    ]

    if skip_confirmation_answer:
        answer_store.add_or_update(
            Answer(answer_id="skip-confirmation-answer", value=skip_confirmation_answer)
        )
        answer_store.add_or_update(Answer(answer_id="security-answer", value="Yes"))

        progress.append(
            {
                "section_id": "skip-confirmation-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["security", "skip-confirmation"],
            }
        )

    progress_store = ProgressStore(progress)

    # When I build the path
    path_finder = PathFinder(
        schema,
        answer_store,
        list_store,
        progress_store,
        metadata={},
        response_metadata={},
    )
    routing_path = path_finder.routing_path(section_id=section_id)

    # Then the path is built correctly
    expected_routing_path = RoutingPath(
        expected_route,
        section_id=section_id,
    )
    assert routing_path == expected_routing_path


@pytest.mark.parametrize(
    "skip_age_answer, expected_route",
    (
        (
            # Answering 'Yes' to the skip age question
            # means in all repeating sections you won't be asked their age
            "Yes",
            ["repeating-sex"],
        ),
        (
            # Answering 'No' to the skip age question
            # means in all repeating sections you will be asked their age
            "No",
            ["repeating-sex", "repeating-age"],
        ),
    ),
)
@pytest.mark.parametrize(
    "schema_name",
    (
        [
            "test_new_routing_and_skipping_section_dependencies",
            "test_routing_and_skipping_section_dependencies",
        ]
    ),
)
def test_routing_path_block_ids_dependent_on_other_sections_when_rules_repeating(
    skip_age_answer, schema_name, expected_route, answer_store
):
    # Given a schema with repeating sections which has when rules dependent on another section
    schema = load_schema_from_name(schema_name)
    answer_store.add_or_update(
        Answer(answer_id="skip-age-answer", value=skip_age_answer)
    )
    answer_store.add_or_update(
        Answer(answer_id="first-name", value="John", list_item_id="lCIZsS")
    )
    answer_store.add_or_update(
        Answer(answer_id="last-name", value="Smith", list_item_id="lCIZsS")
    )

    answer_store.add_or_update(Answer(answer_id="anyone-else", value="No"))

    list_store = ListStore([{"items": ["lCIZsS"], "name": "people"}])

    progress_store = ProgressStore(
        [
            {
                "section_id": "skip-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["skip-age"],
            },
            {
                "section_id": "household-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["list-collector"],
            },
        ]
    )

    # When I build the path
    path_finder = PathFinder(
        schema,
        answer_store,
        list_store,
        progress_store,
        metadata={},
        response_metadata={},
    )
    routing_path = path_finder.routing_path(
        section_id="household-personal-details-section", list_item_id="lCIZsS"
    )

    # Then the path is built correctly
    expected_routing_path = RoutingPath(
        expected_route,
        section_id="household-personal-details-section",
        list_item_id="lCIZsS",
        list_name="people",
    )

    assert routing_path == expected_routing_path
