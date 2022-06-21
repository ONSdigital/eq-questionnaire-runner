from mock import Mock

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.questionnaire.placeholder_parser import PlaceholderParser
from app.questionnaire.questionnaire_schema import QuestionnaireSchema


def test_parse_placeholders(placeholder_list, parser):
    placeholders = parser(placeholder_list)

    assert isinstance(placeholders, dict)
    assert "first_name" in placeholders
    assert placeholders["first_name"] == "Joe"


def test_metadata_placeholder(mock_renderer):
    placeholder_list = [
        {
            "placeholder": "period",
            "value": {"source": "metadata", "identifier": "period_str"},
        }
    ]

    period_str = "Aug 2018"
    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata={"period_str": period_str},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_list)
    assert period_str == placeholders["period"]


def test_previous_answer_transform_placeholder(mock_renderer):
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
                        }
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
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )
    placeholders = parser(placeholder_list)

    assert placeholders["total_turnover"] == "£1,000.00"


def test_metadata_transform_placeholder(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata={"ref_p_start_date": "2019-02-11"},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )
    placeholders = parser(placeholder_list)

    assert placeholders["start_date"] == "Monday 11 February 2019"


def test_response_metadata_transform_placeholder(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata={"ref_p_start_date": "2019-02-11"},
        response_metadata={"started_at": "2019-02-11"},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )
    placeholders = parser(placeholder_list)

    assert placeholders["start_date"] == "Monday 11 February 2019"


def test_multiple_answer_transform_placeholder(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [
                {"answer_id": "first-name", "value": "Joe"},
                {"answer_id": "last-name", "value": "Bloggs"},
            ]
        ),
        list_store=ListStore(),
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_list)

    assert placeholders["persons_name"] == "Joe Bloggs"


def test_first_non_empty_item_transform_placeholder(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata={"ru_name": "ru_name"},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_list)

    assert placeholders["company_name"] == "ru_name"


def test_format_list_answer_transform_placeholder(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [{"answer_id": "checkbox-answer", "value": ["Ham", "Cheese"]}]
        ),
        list_store=ListStore(),
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_list)

    assert placeholders["toppings"] == "<ul><li>Ham</li><li>Cheese</li></ul>"


def test_placeholder_parser_escapes_answers(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "checkbox-answer",
                    "value": ["Cheese & Onion", "Salt & Vinegar", "><'"],
                }
            ]
        ),
        list_store=ListStore(),
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_list)

    assert (
        placeholders["crisps"]
        == "<ul><li>Cheese &amp; Onion</li><li>Salt &amp; Vinegar</li><li>&gt;&lt;&#39;</li></ul>"
    )


def test_multiple_metadata_transform_placeholder(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata={"ref_p_start_date": "2019-02-11"},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_list)

    assert placeholders["start_date"] == "11/02/2019"


def test_multiple_metadata_list_transform_placeholder(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata={"ref_p_start_date": "2019-02-11", "ref_p_end_date": "2019-10-11"},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )
    placeholders = parser(placeholder_list)

    assert placeholders["dates"] == "2019-02-11 2019-10-11"


def test_checkbox_transform_placeholder(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [
                {"answer_id": "checkbox-answer", "value": ["Ham", "Cheese"]},
            ]
        ),
        list_store=ListStore(),
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_list)

    assert placeholders["toppings"] == "Ham, Cheese"


def test_mixed_transform_placeholder(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [{"answer_id": "date-of-birth-answer", "value": "1999-01-01"}]
        ),
        list_store=ListStore(),
        metadata={"second-date": "2019-02-02"},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )
    placeholders = parser(placeholder_list)

    assert placeholders["age"] == "20 years"


def test_mixed_transform_placeholder_value(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [{"answer_id": "date-of-birth-answer", "value": "1999-01-01"}]
        ),
        list_store=ListStore(),
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )
    placeholders = parser(placeholder_list)

    assert placeholders["age"] == "20 years"


def test_list_source_count(mock_renderer):
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
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )
    placeholders = parser(placeholder_list)

    assert placeholders["number_of_people"] == 2


def test_list_source_count_in_transform(mock_renderer):
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
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )
    placeholders = parser(placeholder_list)

    assert placeholders["number_of_people"] == 2


def test_chain_transform_placeholder(mock_renderer):
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

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [
                {"answer_id": "first-name", "value": "Joe"},
                {"answer_id": "last-name", "value": "Bloggs"},
            ]
        ),
        list_store=ListStore(),
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_list)
    assert placeholders["persons_name"] == "Joe Bloggs’"


def test_placeholder_resolves_answer_value_based_on_first_item_in_list(mock_renderer):
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
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_list)
    assert str(placeholders["answer"]) == "Coffee"


def test_placeholder_resolves_list_item_value_based_on_first_item_in_list(
    mock_renderer,
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
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_list)

    assert str(placeholders["first_person_list_item_id"]) == list_store["people"].first


def test_placeholder_resolves_same_name_items(mock_renderer):
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
        metadata={},
        response_metadata={},
        schema=QuestionnaireSchema({}),
        renderer=mock_renderer,
        list_item_id="abc123",
    )

    placeholders = parser(placeholder_list)

    assert placeholders["answer"] == ["abc123", "fgh789"]


def test_placeholder_resolves_name_is_duplicate_chain(mock_schema, mock_renderer):
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
        metadata={},
        response_metadata={},
        schema=mock_schema,
        list_item_id="abc123",
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_transforms)

    assert placeholders["persons_name"] == "Joe Michael Smith"

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=list_store,
        metadata={},
        response_metadata={},
        schema=mock_schema,
        list_item_id="cde456",
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_transforms)

    assert placeholders["persons_name"] == "Marie Smith"


def test_placeholder_resolves_list_has_items_chain(mock_schema, mock_renderer):
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
        metadata={},
        response_metadata={},
        schema=mock_schema,
        list_item_id="abc123",
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_transforms)

    assert placeholders["persons_name"] == "Joe Michael Smith"

    parser = PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=list_store,
        metadata={},
        response_metadata={},
        schema=mock_schema,
        list_item_id="cde456",
        renderer=mock_renderer,
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
    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata={},
        response_metadata={},
        schema=default_placeholder_value_schema,
        renderer=mock_renderer,
    )

    placeholders = parser(placeholder_list)
    assert placeholders["answer_employee"] == "0"
