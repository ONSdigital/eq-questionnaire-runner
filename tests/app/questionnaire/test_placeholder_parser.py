from decimal import Decimal

import pytest
from mock import Mock

from app.data_models import ProgressStore, SupplementaryDataStore
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress import CompletionStatus, ProgressDict
from app.questionnaire import Location
from app.questionnaire.placeholder_parser import PlaceholderParser
from app.utilities.schema import load_schema_from_name
from tests.app.questionnaire.conftest import get_metadata

# pylint: disable=too-many-lines


def test_parse_placeholders(placeholder_list, parser):
    placeholders = parser(placeholder_list)

    assert isinstance(placeholders, dict)
    assert "first_name" in placeholders
    assert placeholders["first_name"] == "Joe"


def test_metadata_placeholder(mock_renderer, mock_schema, mock_location):
    placeholder_list = [
        {
            "placeholder": "period",
            "value": {
                "source": "metadata",
                "identifier": "period_str",
            },
        }
    ]

    period_str = "Aug 2018"

    metadata = get_metadata({"period_str": period_str})
    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata=metadata,
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)
    assert period_str == placeholders["period"]


def test_previous_answer_transform_placeholder(mock_renderer, mock_location):
    schema = load_schema_from_name("test_placeholder_transform")

    placeholder_list = [
        {
            "placeholder": "total_turnover",
            "transforms": [
                {
                    "transform": "format_currency",
                    "arguments": {
                        "number": {
                            "source": "answers",
                            "identifier": "total-retail-turnover-answer",
                        },
                    },
                }
            ],
        }
    ]

    retail_turnover = "1000"

    answer_store = AnswerStore(
        [{"answer_id": "total-retail-turnover-answer", "value": retail_turnover}]
    )

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata=get_metadata(),
        response_metadata={},
        schema=schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )
    placeholders = parser(placeholder_list)

    assert placeholders["total_turnover"] == "£1,000.00"


def test_metadata_transform_placeholder(mock_renderer, mock_schema, mock_location):
    placeholder_list = [
        {
            "placeholder": "start_date",
            "transforms": [
                {
                    "transform": "format_date",
                    "arguments": {
                        "date_to_format": {
                            "source": "metadata",
                            "identifier": "ref_p_start_date",
                        },
                        "date_format": "EEEE d MMMM yyyy",
                    },
                }
            ],
        }
    ]

    metadata = get_metadata({"ref_p_start_date": "2019-02-11"})

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata=metadata,
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )
    placeholders = parser(placeholder_list)

    assert placeholders["start_date"] == "Monday 11 February 2019"


def test_response_metadata_transform_placeholder(
    mock_renderer, mock_schema, mock_location
):
    # This test should use ISO format dates when they become supported
    placeholder_list = [
        {
            "placeholder": "start_date",
            "transforms": [
                {
                    "transform": "format_date",
                    "arguments": {
                        "date_to_format": {
                            "source": "response_metadata",
                            "identifier": "started_at",
                        },
                        "date_format": "EEEE d MMMM yyyy",
                    },
                }
            ],
        }
    ]

    metadata = get_metadata({"ref_p_start_date": "2019-02-11"})
    response_metadata = {"started_at": "2019-02-11"}

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata=metadata,
        response_metadata=response_metadata,
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )
    placeholders = parser(placeholder_list)

    assert placeholders["start_date"] == "Monday 11 February 2019"


def test_multiple_answer_transform_placeholder(
    mock_renderer, mock_schema, mock_location
):
    placeholder_list = [
        {
            "placeholder": "persons_name",
            "transforms": [
                {
                    "transform": "concatenate_list",
                    "arguments": {
                        "list_to_concatenate": [
                            {"source": "answers", "identifier": "first-name"},
                            {"source": "answers", "identifier": "last-name"},
                        ],
                        "delimiter": " ",
                    },
                }
            ],
        }
    ]

    answer_store = AnswerStore(
        [
            {"answer_id": "first-name", "value": "Joe"},
            {"answer_id": "last-name", "value": "Bloggs"},
        ]
    )

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)

    assert placeholders["persons_name"] == "Joe Bloggs"


def test_first_non_empty_item_transform_placeholder(
    mock_renderer, mock_schema, mock_location
):
    placeholder_list = [
        {
            "placeholder": "company_name",
            "transforms": [
                {
                    "transform": "first_non_empty_item",
                    "arguments": {
                        "items": [
                            {"source": "metadata", "identifier": "trad_as"},
                            {"source": "metadata", "identifier": "ru_name"},
                        ]
                    },
                }
            ],
        }
    ]

    metadata = get_metadata({"trad_as": None, "ru_name": "ru_name"})

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata=metadata,
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)

    assert placeholders["company_name"] == "ru_name"


def test_format_list_answer_transform_placeholder(
    mock_renderer, mock_schema, mock_location
):
    placeholder_list = [
        {
            "placeholder": "toppings",
            "transforms": [
                {
                    "transform": "format_list",
                    "arguments": {
                        "list_to_format": {
                            "source": "answers",
                            "identifier": "checkbox-answer",
                        }
                    },
                }
            ],
        }
    ]

    answer_store = AnswerStore(
        [{"answer_id": "checkbox-answer", "value": ["Ham", "Cheese"]}]
    )

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)

    assert placeholders["toppings"] == "<ul><li>Ham</li><li>Cheese</li></ul>"


def test_placeholder_parser_escapes_answers(mock_renderer, mock_schema, mock_location):
    placeholder_list = [
        {
            "placeholder": "crisps",
            "transforms": [
                {
                    "transform": "format_list",
                    "arguments": {
                        "list_to_format": {
                            "source": "answers",
                            "identifier": "checkbox-answer",
                        }
                    },
                }
            ],
        }
    ]

    answer_store = AnswerStore(
        [
            {
                "answer_id": "checkbox-answer",
                "value": ["Cheese & Onion", "Salt & Vinegar", "><'"],
            }
        ]
    )

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)

    assert (
        placeholders["crisps"]
        == "<ul><li>Cheese &amp; Onion</li><li>Salt &amp; Vinegar</li><li>&gt;&lt;&#39;</li></ul>"
    )


def test_multiple_metadata_transform_placeholder(
    mock_renderer, mock_schema, mock_location
):
    placeholder_list = [
        {
            "placeholder": "start_date",
            "transforms": [
                {
                    "transform": "format_date",
                    "arguments": {
                        "date_to_format": {
                            "source": "metadata",
                            "identifier": "ref_p_start_date",
                        },
                        "date_format": "yyyy-MM-dd",
                    },
                },
                {
                    "transform": "format_date",
                    "arguments": {
                        "date_to_format": {"source": "previous_transform"},
                        "date_format": "dd/MM/yyyy",
                    },
                },
            ],
        }
    ]

    metadata = get_metadata({"ref_p_start_date": "2019-02-11"})

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata=metadata,
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)

    assert placeholders["start_date"] == "11/02/2019"


def test_multiple_metadata_list_transform_placeholder(
    mock_renderer, mock_schema, mock_location
):
    placeholder_list = [
        {
            "placeholder": "dates",
            "transforms": [
                {
                    "transform": "concatenate_list",
                    "arguments": {
                        "list_to_concatenate": [
                            {"source": "metadata", "identifier": "ref_p_start_date"},
                            {"source": "metadata", "identifier": "ref_p_end_date"},
                        ],
                        "delimiter": " ",
                    },
                }
            ],
        }
    ]

    metadata = get_metadata(
        {"ref_p_start_date": "2019-02-11", "ref_p_end_date": "2019-10-11"}
    )

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata=metadata,
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )
    placeholders = parser(placeholder_list)

    assert placeholders["dates"] == "2019-02-11 2019-10-11"


def test_checkbox_transform_placeholder(mock_renderer, mock_schema, mock_location):
    placeholder_list = [
        {
            "placeholder": "toppings",
            "transforms": [
                {
                    "transform": "concatenate_list",
                    "arguments": {
                        "list_to_concatenate": [
                            {"source": "answers", "identifier": "checkbox-answer"}
                        ],
                        "delimiter": ", ",
                    },
                }
            ],
        }
    ]

    answer_store = AnswerStore(
        [
            {"answer_id": "checkbox-answer", "value": ["Ham", "Cheese"]},
        ]
    )

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)

    assert placeholders["toppings"] == "Ham, Cheese"


def test_mixed_transform_placeholder(mock_renderer, mock_schema, mock_location):
    placeholder_list = [
        {
            "placeholder": "age",
            "transforms": [
                {
                    "transform": "calculate_date_difference",
                    "arguments": {
                        "first_date": {
                            "source": "answers",
                            "identifier": "date-of-birth-answer",
                        },
                        "second_date": {
                            "source": "metadata",
                            "identifier": "second-date",
                        },
                    },
                }
            ],
        }
    ]

    answer_store = AnswerStore(
        [{"answer_id": "date-of-birth-answer", "value": "1999-01-01"}]
    )
    metadata = get_metadata({"second-date": "2019-02-02"})

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata=metadata,
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )
    placeholders = parser(placeholder_list)

    assert placeholders["age"] == "20 years"


def test_mixed_transform_placeholder_value(mock_renderer, mock_schema, mock_location):
    placeholder_list = [
        {
            "placeholder": "age",
            "transforms": [
                {
                    "transform": "calculate_date_difference",
                    "arguments": {
                        "first_date": {
                            "source": "answers",
                            "identifier": "date-of-birth-answer",
                        },
                        "second_date": {"value": "2019-02-02"},
                    },
                }
            ],
        }
    ]

    answer_store = AnswerStore(
        [{"answer_id": "date-of-birth-answer", "value": "1999-01-01"}]
    )

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )
    placeholders = parser(placeholder_list)

    assert placeholders["age"] == "20 years"


def test_list_source_count(mock_renderer, mock_schema, mock_location):
    placeholder_list = [
        {
            "placeholder": "number_of_people",
            "value": {"source": "list", "identifier": "people", "selector": "count"},
        }
    ]

    list_store = ListStore()
    list_store.add_list_item("people")
    list_store.add_list_item("people")

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=list_store,
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )
    placeholders = parser(placeholder_list)

    assert placeholders["number_of_people"] == 2


def test_list_source_count_in_transform(mock_renderer, mock_schema, mock_location):
    placeholder_list = [
        {
            "placeholder": "number_of_people",
            "transforms": [
                {
                    "transform": "add",
                    "arguments": {
                        "lhs": {
                            "source": "list",
                            "identifier": "people",
                            "selector": "count",
                        },
                        "rhs": {"value": 1},
                    },
                }
            ],
        }
    ]

    list_store = ListStore()
    list_store.add_list_item("people")

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=list_store,
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )
    placeholders = parser(placeholder_list)

    assert placeholders["number_of_people"] == 2


def test_chain_transform_placeholder(mock_renderer, mock_schema, mock_location):
    placeholder_list = [
        {
            "placeholder": "persons_name",
            "transforms": [
                {
                    "transform": "concatenate_list",
                    "arguments": {
                        "list_to_concatenate": [
                            {"source": "answers", "identifier": "first-name"},
                            {"source": "answers", "identifier": "last-name"},
                        ],
                        "delimiter": " ",
                    },
                },
                {
                    "transform": "format_possessive",
                    "arguments": {"string_to_format": {"source": "previous_transform"}},
                },
            ],
        }
    ]

    answer_store = AnswerStore(
        [
            {"answer_id": "first-name", "value": "Joe"},
            {"answer_id": "last-name", "value": "Bloggs"},
        ]
    )

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)
    assert placeholders["persons_name"] == "Joe Bloggs’"


def test_placeholder_resolves_answer_value_based_on_first_item_in_list(
    mock_renderer, mock_schema, mock_location
):
    placeholder_list = [
        {
            "placeholder": "answer",
            "value": {
                "source": "answers",
                "identifier": "favourite-drink-answer",
                "list_item_selector": {
                    "source": "list",
                    "identifier": "people",
                    "selector": "first",
                },
            },
        }
    ]

    list_store = ListStore([{"items": ["abc123", "123abc"], "name": "people"}])

    answer_store = AnswerStore(
        [
            {
                "answer_id": "favourite-drink-answer",
                "value": "Coffee",
                "list_item_id": "abc123",
            }
        ]
    )

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=list_store,
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)
    assert str(placeholders["answer"]) == "Coffee"


def test_placeholder_resolves_list_item_value_based_on_first_item_in_list(
    mock_renderer, mock_schema, mock_location
):
    placeholder_list = [
        {
            "placeholder": "first_person_list_item_id",
            "value": {
                "source": "list",
                "selector": "first",
                "identifier": "people",
            },
        }
    ]

    list_store = ListStore([{"items": ["item-1", "item-2"], "name": "people"}])

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=list_store,
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)

    assert str(placeholders["first_person_list_item_id"]) == list_store["people"].first


def test_placeholder_resolves_same_name_items(
    mock_renderer, mock_schema, mock_location
):
    list_store = ListStore(
        [
            {
                "items": ["abc123", "cde456", "fgh789"],
                "same_name_items": ["abc123", "fgh789"],
                "name": "people",
            }
        ]
    )
    placeholder_list = [
        {
            "placeholder": "answer",
            "value": {
                "source": "list",
                "selector": "same_name_items",
                "identifier": "people",
            },
        },
    ]

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=list_store,
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        list_item_id="abc123",
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)

    assert placeholders["answer"] == ["abc123", "fgh789"]


def test_placeholder_resolves_name_is_duplicate_chain(
    mock_schema, mock_renderer, mock_location
):
    list_store = ListStore(
        [
            {
                "items": ["abc123", "cde456", "fgh789"],
                "same_name_items": ["abc123", "fgh789"],
                "name": "people",
            }
        ]
    )
    answer_store = AnswerStore(
        [
            {
                "answer_id": "first-name-answer",
                "value": "Joe",
                "list_item_id": "abc123",
            },
            {
                "answer_id": "middle-names-answer",
                "value": "Michael",
                "list_item_id": "abc123",
            },
            {
                "answer_id": "last-name-answer",
                "value": "Smith",
                "list_item_id": "abc123",
            },
            {
                "answer_id": "first-name-answer",
                "value": "Marie",
                "list_item_id": "cde456",
            },
            {
                "answer_id": "middle-names-answer",
                "value": "Jane",
                "list_item_id": "cde456",
            },
            {
                "answer_id": "last-name-answer",
                "value": "Smith",
                "list_item_id": "cde456",
            },
        ]
    )
    placeholder_transforms = [
        {
            "placeholder": "persons_name",
            "transforms": [
                {
                    "transform": "contains",
                    "arguments": {
                        "list_to_check": {
                            "source": "list",
                            "selector": "same_name_items",
                            "identifier": "people",
                        },
                        "value": {
                            "source": "location",
                            "identifier": "list_item_id",
                        },
                    },
                },
                {
                    "transform": "format_name",
                    "arguments": {
                        "include_middle_names": {"source": "previous_transform"},
                        "first_name": {
                            "source": "answers",
                            "identifier": "first-name-answer",
                        },
                        "middle_names": {
                            "source": "answers",
                            "identifier": "middle-names-answer",
                        },
                        "last_name": {
                            "source": "answers",
                            "identifier": "last-name-answer",
                        },
                    },
                },
            ],
        }
    ]

    mock_schema.is_repeating_answer = Mock(return_value=True)

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=list_store,
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        list_item_id="abc123",
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_transforms)

    assert placeholders["persons_name"] == "Joe Michael Smith"

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=list_store,
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        list_item_id="cde456",
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_transforms)

    assert placeholders["persons_name"] == "Marie Smith"


def test_placeholder_resolves_list_has_items_chain(
    mock_schema, mock_renderer, mock_location
):
    list_store = ListStore(
        [
            {
                "items": ["abc123", "cde456", "fgh789"],
                "same_name_items": ["abc123", "fgh789"],
                "name": "people",
            }
        ]
    )
    answer_store = AnswerStore(
        [
            {
                "answer_id": "first-name-answer",
                "value": "Joe",
                "list_item_id": "abc123",
            },
            {
                "answer_id": "middle-names-answer",
                "value": "Michael",
                "list_item_id": "abc123",
            },
            {
                "answer_id": "last-name-answer",
                "value": "Smith",
                "list_item_id": "abc123",
            },
            {
                "answer_id": "first-name-answer",
                "value": "Marie",
                "list_item_id": "cde456",
            },
            {
                "answer_id": "middle-names-answer",
                "value": "Jane",
                "list_item_id": "cde456",
            },
            {
                "answer_id": "last-name-answer",
                "value": "Smith",
                "list_item_id": "cde456",
            },
        ]
    )
    placeholder_transforms = [
        {
            "placeholder": "persons_name",
            "transforms": [
                {
                    "transform": "list_has_items",
                    "arguments": {
                        "list_to_check": {
                            "source": "list",
                            "selector": "same_name_items",
                            "identifier": "people",
                        },
                    },
                },
                {
                    "transform": "format_name",
                    "arguments": {
                        "include_middle_names": {"source": "previous_transform"},
                        "first_name": {
                            "source": "answers",
                            "identifier": "first-name-answer",
                        },
                        "middle_names": {
                            "source": "answers",
                            "identifier": "middle-names-answer",
                        },
                        "last_name": {
                            "source": "answers",
                            "identifier": "last-name-answer",
                        },
                    },
                },
            ],
        }
    ]

    mock_schema.is_repeating_answer = Mock(return_value=True)

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=list_store,
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        list_item_id="abc123",
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_transforms)

    assert placeholders["persons_name"] == "Joe Michael Smith"

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=list_store,
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        list_item_id="cde456",
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_transforms)

    assert placeholders["persons_name"] == "Marie Jane Smith"


def test_placeholder_default_value(default_placeholder_value_schema, mock_renderer):
    placeholder_list = [
        {
            "placeholder": "answer_employee",
            "transforms": [
                {
                    "transform": "format_number",
                    "arguments": {
                        "number": {"source": "answers", "identifier": "employees-no"}
                    },
                }
            ],
        }
    ]

    location = Location(section_id="default-section")

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata=get_metadata(),
        response_metadata={},
        schema=default_placeholder_value_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)
    assert placeholders["answer_employee"] == "0"


def test_placeholder_parser_calculated_summary_dependencies_cache(
    mocker, mock_renderer
):
    """
    Tests Calculated Summaries fetches the dependencies using the routing path cache
    Mocker patch the routing_path function in the Path Finder class to check the number of calls
    Both placeholders lists use the calculated summary placeholder that requires the Path.
    The first and second placeholder list is from the same section so when we call the second list, it should use the cache from the first call.
    Set Location to the BlockId where the transform is required and the values have already been set
    Set Answer Store with values to check if the transform is working as expected in the Schema.
    With calculated summaries we check the two values in the answer source sum to the expected number
    """
    schema = load_schema_from_name("test_calculated_summary")

    path_finder = mocker.patch("app.questionnaire.path_finder.PathFinder.routing_path")

    placeholder_list_1 = [
        {
            "placeholder": "percentage-total-playback",
            "value": {
                "source": "calculated_summary",
                "identifier": "percentage-total-playback",
            },
        },
    ]

    placeholder_list_2 = [
        {
            "placeholder": "unit-total-playback",
            "value": {
                "source": "calculated_summary",
                "identifier": "unit-total-playback",
            },
        },
    ]

    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="default-section",
                block_ids=[
                    "second-number-answer-unit-total",
                    "third-and-a-half-number-answer-unit-total",
                    "unit-total-playback",
                    "fifth-percent-answer",
                    "sixth-percent-answer",
                    "percentage-total-playback",
                ],
                status="COMPLETED",
            ),
        ]
    )

    answer_store = AnswerStore(
        [
            {"answer_id": "second-number-answer-unit-total", "value": 1},
            {"answer_id": "third-and-a-half-number-answer-unit-total", "value": 10},
            {"answer_id": "fifth-percent-answer", "value": 2},
            {"answer_id": "sixth-percent-answer", "value": 20},
        ]
    )

    location = Location(
        section_id="default-section",
        block_id="calculated-summary-total-confirmation",
    )

    placeholder_parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata=get_metadata(),
        response_metadata={},
        schema=schema,
        renderer=mock_renderer,
        progress_store=progress_store,
        location=location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholder_1 = placeholder_parser(placeholder_list=placeholder_list_1)
    assert placeholder_1["percentage-total-playback"] == 22
    assert path_finder.called == 1

    placeholder_2 = placeholder_parser(placeholder_list=placeholder_list_2)
    assert placeholder_2["unit-total-playback"] == 11
    assert path_finder.called == 1


def test_placeholder_dependencies_cache(mocker, mock_renderer):
    """
    Tests Placeholder Parser fetches the placeholder dependencies using the routing path cache
    Mocker patch the routing_path function in the Path Finder class to check the number of calls
    Both placeholders lists use the first_non_empty_item transform that requires the Path.
    The first and second placeholder list is from the same section so when we call the second list, it should use the cache from the first call.
    Set Location to the BlockId where the transform is required and the values have already been set
    Set Answer Store with values to check if the transform is working as expected in the Schema.
    """
    schema = load_schema_from_name("test_placeholder_first_non_empty_item")
    path_finder = mocker.patch("app.questionnaire.path_finder.PathFinder.routing_path")
    placeholder_list_1 = [
        {
            "placeholder": "date_entry_answer_from",
            "transforms": [
                {
                    "transform": "first_non_empty_item",
                    "arguments": {
                        "items": [
                            {
                                "source": "answers",
                                "identifier": "date-entry-answer-from",
                            },
                            {"source": "metadata", "identifier": "ref_p_start_date"},
                        ]
                    },
                },
                {
                    "transform": "format_date",
                    "arguments": {
                        "date_to_format": {"source": "previous_transform"},
                        "date_format": "d MMMM yyyy",
                    },
                },
            ],
        }
    ]

    placeholder_list_2 = [
        {
            "placeholder": "date_entry_answer_to",
            "transforms": [
                {
                    "transform": "first_non_empty_item",
                    "arguments": {
                        "items": [
                            {"source": "answers", "identifier": "date-entry-answer-to"},
                            {"source": "metadata", "identifier": "ref_p_end_date"},
                        ]
                    },
                },
                {
                    "transform": "format_date",
                    "arguments": {
                        "date_to_format": {"source": "previous_transform"},
                        "date_format": "d MMMM yyyy",
                    },
                },
            ],
        },
        {
            "placeholder": "ru_name",
            "value": {"source": "metadata", "identifier": "ru_name"},
        },
    ]

    location = Location(
        section_id="default-section",
        block_id="total-turnover-block",
    )

    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="default-section",
                block_ids=["date-question-block", "date-entry-block"],
                status=CompletionStatus.COMPLETED,
            )
        ]
    )
    answer_store = AnswerStore(
        [
            {"answer_id": "date-entry-answer-from", "value": "2016-04-16"},
            {"answer_id": "date-entry-answer-to", "value": "2016-04-28"},
        ]
    )
    placeholder_parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata=get_metadata(),
        response_metadata={},
        schema=schema,
        renderer=mock_renderer,
        progress_store=progress_store,
        location=location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholder_1 = placeholder_parser(placeholder_list=placeholder_list_1)
    assert placeholder_1["date_entry_answer_from"] == "16 April 2016"
    assert path_finder.called == 1

    placeholder_2 = placeholder_parser(placeholder_list=placeholder_list_2)
    assert placeholder_2["date_entry_answer_to"] == "28 April 2016"
    assert path_finder.called == 1


@pytest.mark.parametrize(
    "first_number, second_number, expected_result",
    (
        ("1.2", "1", "£2.20"),
        ("1", "2", "£3"),
        ("1.123", "1.2", "£2.323"),
    ),
)
def test_format_currency_placeholder_total_with_previous_transform(
    mock_renderer,
    mock_schema,
    mock_location,
    first_number,
    second_number,
    expected_result,
):
    placeholder_list = [
        {
            "placeholder": "total",
            "transforms": [
                {
                    "transform": "add",
                    "arguments": {
                        "lhs": Decimal(first_number),
                        "rhs": Decimal(second_number),
                    },
                },
                {
                    "transform": "format_currency",
                    "arguments": {"number": {"source": "previous_transform"}},
                },
            ],
        }
    ]

    metadata = get_metadata()

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata=metadata,
        response_metadata={},
        schema=mock_schema,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
        location=mock_location,
        supplementary_data_store=SupplementaryDataStore(),
    )

    placeholders = parser(placeholder_list)

    assert placeholders["total"] == expected_result
