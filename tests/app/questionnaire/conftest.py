# pylint: disable=redefined-outer-name
from unittest.mock import Mock

import pytest
from werkzeug.datastructures import ImmutableDict

from app.data_models import QuestionnaireStore
from app.data_models.answer_store import Answer, AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import Location
from app.questionnaire.placeholder_parser import PlaceholderParser
from app.questionnaire.placeholder_renderer import (
    PlaceholderRenderer,
    find_pointers_containing,
)
from app.questionnaire.placeholder_transforms import PlaceholderTransforms
from app.questionnaire.routing_path import RoutingPath
from app.utilities.schema import load_schema_from_name


@pytest.fixture
def placeholder_list():
    return [
        {
            "placeholder": "first_name",
            "value": {"source": "answers", "identifier": "first-name"},
        }
    ]


@pytest.fixture
def answer_store():
    return AnswerStore([{"answer_id": "first-name", "value": "Joe"}])


@pytest.fixture
def location():
    return Location("test-section", "test-block", "test-list", "list_item_id")


@pytest.fixture
def response_metadata():
    return {"started_at": "2021-01-01T09:00:00.220038+00:00"}


@pytest.fixture
def parser(answer_store, location, mock_schema, mock_renderer):
    return PlaceholderParser(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata={},
        response_metadata={},
        schema=mock_schema,
        location=location,
        renderer=mock_renderer,
    )


@pytest.fixture()
def question_variant_schema():
    return {
        "sections": [
            {
                "id": "section1",
                "groups": [
                    {
                        "id": "group1",
                        "title": "Group 1",
                        "blocks": [
                            {
                                "id": "block1",
                                "type": "Question",
                                "title": "Block 1",
                                "question_variants": [
                                    {
                                        "when": [
                                            {
                                                "id": "when-answer",
                                                "condition": "equals",
                                                "value": "yes",
                                            }
                                        ],
                                        "question": {
                                            "id": "question1",
                                            "title": "Question 1, Yes",
                                            "answers": [
                                                {
                                                    "id": "answer1",
                                                    "label": "Answer 1 Variant 1",
                                                }
                                            ],
                                        },
                                    },
                                    {
                                        "when": [
                                            {
                                                "id": "when-answer",
                                                "condition": "not equals",
                                                "value": "yes",
                                            }
                                        ],
                                        "question": {
                                            "id": "question1",
                                            "title": "Question 1, No",
                                            "answers": [
                                                {
                                                    "id": "answer1",
                                                    "label": "Answer 1 Variant 2",
                                                }
                                            ],
                                        },
                                    },
                                ],
                            }
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture()
def single_question_schema():
    return {
        "sections": [
            {
                "id": "section1",
                "title": "Section 1",
                "groups": [
                    {
                        "id": "group1",
                        "title": "Group 1",
                        "blocks": [
                            {
                                "id": "block1",
                                "type": "Question",
                                "title": "Block 1",
                                "question": {
                                    "id": "question1",
                                    "title": "Question 1",
                                    "answers": [
                                        {
                                            "id": "answer1",
                                            "label": "Answer 1",
                                            "default": "test",
                                        }
                                    ],
                                },
                            }
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture()
def list_collector_variant_schema():
    return {
        "sections": [
            {
                "id": "section",
                "groups": [
                    {
                        "id": "group",
                        "title": "List",
                        "blocks": [
                            {
                                "id": "block1",
                                "type": "ListCollector",
                                "for_list": "people",
                                "question_variants": [
                                    {
                                        "question": {
                                            "id": "confirmation-question",
                                            "type": "General",
                                            "title": "Collector, Yes",
                                            "answers": [
                                                {
                                                    "id": "answer1",
                                                    "label": "Collector Answer 1 Variant Yes",
                                                    "action": {
                                                        "type": "RedirectToListAddBlock"
                                                    },
                                                }
                                            ],
                                        },
                                        "when": [
                                            {
                                                "id": "when-answer",
                                                "condition": "equals",
                                                "value": "yes",
                                            }
                                        ],
                                    },
                                    {
                                        "question": {
                                            "id": "confirmation-question",
                                            "type": "General",
                                            "title": "Collector, No",
                                            "answers": [
                                                {
                                                    "id": "answer1",
                                                    "label": "Collector Answer 1 Variant No",
                                                }
                                            ],
                                        },
                                        "when": [
                                            {
                                                "id": "when-answer",
                                                "condition": "equals",
                                                "value": "no",
                                            }
                                        ],
                                    },
                                ],
                                "add_block": {
                                    "id": "add-person",
                                    "type": "Question",
                                    "question_variants": [
                                        {
                                            "question": {
                                                "id": "add-question",
                                                "type": "General",
                                                "title": "Add, Yes",
                                                "answers": [
                                                    {
                                                        "id": "answer1",
                                                        "label": "Answer 1 Variant Yes",
                                                    }
                                                ],
                                            },
                                            "when": [
                                                {
                                                    "id": "when-answer",
                                                    "condition": "equals",
                                                    "value": "yes",
                                                }
                                            ],
                                        },
                                        {
                                            "question": {
                                                "id": "add-question",
                                                "type": "General",
                                                "title": "Add, No",
                                                "answers": [
                                                    {
                                                        "id": "answer1",
                                                        "label": "Answer 1 Variant Yes",
                                                    }
                                                ],
                                            },
                                            "when": [
                                                {
                                                    "id": "when-answer",
                                                    "condition": "equals",
                                                    "value": "no",
                                                }
                                            ],
                                        },
                                    ],
                                },
                                "edit_block": {
                                    "id": "edit-person",
                                    "type": "Question",
                                    "question_variants": [
                                        {
                                            "question": {
                                                "id": "edit-question",
                                                "type": "General",
                                                "title": "Edit, Yes",
                                                "answers": [
                                                    {
                                                        "id": "answer1",
                                                        "label": "Answer 1 Variant Yes",
                                                    }
                                                ],
                                            },
                                            "when": [
                                                {
                                                    "id": "when-answer",
                                                    "condition": "equals",
                                                    "value": "yes",
                                                }
                                            ],
                                        },
                                        {
                                            "question": {
                                                "id": "edit-question",
                                                "type": "General",
                                                "title": "Edit, No",
                                                "answers": [
                                                    {
                                                        "id": "answer1",
                                                        "label": "Answer 1 Variant No",
                                                    }
                                                ],
                                            },
                                            "when": [
                                                {
                                                    "id": "when-answer",
                                                    "condition": "equals",
                                                    "value": "no",
                                                }
                                            ],
                                        },
                                    ],
                                },
                                "remove_block": {
                                    "id": "remove-person",
                                    "type": "Question",
                                    "question_variants": [
                                        {
                                            "question": {
                                                "id": "remove-question",
                                                "type": "General",
                                                "title": "Remove, Yes",
                                                "answers": [
                                                    {
                                                        "id": "answer1",
                                                        "label": "Answer 1 Variant Yes",
                                                        "action": {
                                                            "type": "RemoveListItemAndAnswers"
                                                        },
                                                    }
                                                ],
                                            },
                                            "when": [
                                                {
                                                    "id": "when-answer",
                                                    "condition": "equals",
                                                    "value": "yes",
                                                }
                                            ],
                                        },
                                        {
                                            "question": {
                                                "id": "remove-question",
                                                "type": "General",
                                                "title": "Remove, No",
                                                "answers": [
                                                    {
                                                        "id": "answer1",
                                                        "label": "Answer 1 Variant No",
                                                    }
                                                ],
                                            },
                                            "when": [
                                                {
                                                    "id": "when-answer",
                                                    "condition": "equals",
                                                    "value": "no",
                                                }
                                            ],
                                        },
                                    ],
                                },
                            }
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture
def sections_dependent_on_list_schema():
    return {
        "sections": [
            {
                "id": "section1",
                "groups": [
                    {
                        "id": "group1",
                        "blocks": [
                            {
                                "id": "list-collector",
                                "type": "ListCollector",
                                "for_list": "list",
                                "question": {},
                                "add_block": {
                                    "id": "add-block",
                                    "type": "ListAddQuestion",
                                    "question": {},
                                },
                                "edit_block": {
                                    "id": "edit-block",
                                    "type": "ListEditQuestion",
                                    "question": {},
                                },
                                "remove_block": {
                                    "id": "remove-block",
                                    "type": "ListRemoveQuestion",
                                    "question": {},
                                },
                            }
                        ],
                    }
                ],
            },
            {
                "id": "section2",
                "groups": [
                    {
                        "id": "group2",
                        "blocks": [
                            {
                                "type": "Interstitial",
                                "id": "household-occupance",
                                "content_variants": [
                                    {
                                        "content": {
                                            "title": "Household Occupance",
                                            "contents": [
                                                {
                                                    "description": "According to your answer this household is occupied"
                                                }
                                            ],
                                        },
                                        "when": {
                                            ">": [
                                                0,
                                                {
                                                    "count": [
                                                        {
                                                            "source": "list",
                                                            "identifier": "list",
                                                        }
                                                    ]
                                                },
                                            ]
                                        },
                                    },
                                    {
                                        "content": {
                                            "title": "Household Occupance",
                                            "contents": [
                                                {
                                                    "description": "According to your answer this household is unoccupied"
                                                }
                                            ],
                                        },
                                        "when": {
                                            "==": [
                                                0,
                                                {
                                                    "count": [
                                                        {
                                                            "source": "list",
                                                            "identifier": "list",
                                                        }
                                                    ]
                                                },
                                            ]
                                        },
                                    },
                                ],
                            },
                            {
                                "type": "Question",
                                "id": "block2",
                                "question": {
                                    "answers": [
                                        {
                                            "id": "answer1",
                                            "mandatory": True,
                                            "type": "General",
                                        }
                                    ],
                                    "id": "question1",
                                    "title": {"text": "Does anyone else live here?"},
                                    "type": "General",
                                },
                                "when": {
                                    ">": [
                                        0,
                                        {
                                            "count": [
                                                {
                                                    "source": "list",
                                                    "identifier": "list",
                                                }
                                            ]
                                        },
                                    ]
                                },
                            },
                        ],
                    }
                ],
            },
            {
                "id": "section3",
                "groups": [
                    {
                        "id": "group3",
                        "blocks": [
                            {
                                "type": "Question",
                                "id": "block3",
                                "question": {
                                    "answers": [
                                        {
                                            "id": "answer1",
                                            "mandatory": True,
                                            "type": "General",
                                        }
                                    ],
                                    "id": "question1",
                                    "title": {"text": "Does anyone else live here?"},
                                    "type": "General",
                                },
                                "when": [
                                    {
                                        "condition": "greater than",
                                        "list": "not-the-list",
                                        "value": 0,
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                "id": "section4",
                "groups": [
                    {
                        "id": "group4",
                        "blocks": [
                            {
                                "type": "Question",
                                "id": "block4",
                                "question": {
                                    "answers": [
                                        {
                                            "id": "answer1",
                                            "mandatory": True,
                                            "type": "General",
                                        }
                                    ],
                                    "id": "question1",
                                    "title": {"text": "Does anyone else live here?"},
                                    "type": "General",
                                },
                                "when": [
                                    {
                                        "condition": "greater than",
                                        "list": "list",
                                        "value": 0,
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                "id": "section5",
                "groups": [
                    {
                        "id": "group5",
                        "blocks": [
                            {
                                "type": "Question",
                                "id": "block5",
                                "question": {
                                    "answers": [
                                        {
                                            "id": "answer1",
                                            "mandatory": True,
                                            "type": "General",
                                        }
                                    ],
                                    "id": "question1",
                                    "title": {"text": "Does anyone else live here?"},
                                    "type": "General",
                                },
                                "when": {
                                    ">": [
                                        {
                                            "count": [
                                                {
                                                    "source": "list",
                                                    "identifier": "not-a-list",
                                                }
                                            ]
                                        },
                                        0,
                                    ]
                                },
                            }
                        ],
                    }
                ],
            },
        ]
    }


@pytest.fixture()
def content_variant_schema():
    return {
        "sections": [
            {
                "id": "section1",
                "groups": [
                    {
                        "id": "group1",
                        "title": "Group 1",
                        "blocks": [
                            {
                                "id": "block1",
                                "type": "Question",
                                "title": "Block 1",
                                "content_variants": [
                                    {
                                        "content": [{"title": "You are over 16"}],
                                        "when": [
                                            {
                                                "id": "age-answer",
                                                "condition": "greater than",
                                                "value": "16",
                                            }
                                        ],
                                    },
                                    {
                                        "content": [{"title": "You are under 16"}],
                                        "when": [
                                            {
                                                "id": "age-answer",
                                                "condition": "less than or equal to",
                                                "value": "16",
                                            }
                                        ],
                                    },
                                    {
                                        "content": [{"title": "You are ageless"}],
                                        "when": [
                                            {"id": "age-answer", "condition": "not set"}
                                        ],
                                    },
                                ],
                            }
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture()
def question_schema():
    return {
        "sections": [
            {
                "id": "section1",
                "groups": [
                    {
                        "id": "group1",
                        "title": "Group 1",
                        "blocks": [
                            {
                                "id": "block1",
                                "type": "Question",
                                "title": "Block 1",
                                "question": {
                                    "id": "question1",
                                    "title": "A Question",
                                    "answers": [{"id": "answer1", "label": "Answer 1"}],
                                },
                            }
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture()
def mock_relationship_collector_schema():
    return {
        "sections": [
            {
                "id": "section",
                "groups": [
                    {
                        "id": "group",
                        "title": "List",
                        "blocks": [
                            {
                                "type": "RelationshipCollector",
                                "id": "relationships",
                                "for_list": "people",
                                "question": {},
                            },
                            {
                                "type": "RelationshipCollector",
                                "id": "not-people-relationship-collector",
                                "for_list": "not-people",
                                "question": {},
                            },
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture()
def section_with_custom_summary():
    return {
        "sections": [
            {
                "id": "section",
                "summary": {
                    "show_on_completion": True,
                    "items": [
                        {
                            "type": "List",
                            "for_list": "people",
                            "title": "Householders",
                            "add_link_text": "Add a person",
                            "empty_list_text": "No householders",
                            "item_title": {
                                "text": "{person_name}",
                                "placeholders": [
                                    {
                                        "placeholder": "person_name",
                                        "transforms": [
                                            {
                                                "arguments": {
                                                    "delimiter": " ",
                                                    "list_to_concatenate": [
                                                        {
                                                            "source": "answers",
                                                            "identifier": "first-name",
                                                        },
                                                        {
                                                            "source": "answers",
                                                            "identifier": "last-name",
                                                        },
                                                    ],
                                                },
                                                "transform": "concatenate_list",
                                            }
                                        ],
                                    }
                                ],
                            },
                        }
                    ],
                },
                "groups": [
                    {
                        "id": "group",
                        "title": "List",
                        "blocks": [
                            {
                                "type": "RelationshipCollector",
                                "id": "relationships",
                                "for_list": "people",
                                "question": {},
                            },
                            {
                                "type": "RelationshipCollector",
                                "id": "not-people-relationship-collector",
                                "for_list": "not-people",
                                "question": {},
                            },
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture
def section_with_repeating_list():
    return {
        "sections": [
            {
                "id": "personal-details-section",
                "title": "Personal Details",
                "repeat": {"for_list": "people"},
                "groups": [
                    {
                        "id": "personal-details-group",
                        "title": "Personal Details",
                        "blocks": [
                            {
                                "id": "proxy",
                                "question": {
                                    "answers": [
                                        {
                                            "default": "Yes",
                                            "id": "proxy-answer",
                                            "mandatory": False,
                                            "options": [
                                                {
                                                    "label": "No, I’m answering for myself",
                                                    "value": "No",
                                                },
                                                {"label": "Yes", "value": "Yes"},
                                            ],
                                            "type": "Radio",
                                        }
                                    ],
                                    "id": "proxy-question",
                                    "title": "Are you answering the questions on behalf of someone else?",
                                    "type": "General",
                                },
                                "type": "Question",
                            }
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture
def mock_schema():
    schema = Mock(
        QuestionnaireSchema(
            {
                "questionnaire_flow": {
                    "type": "Linear",
                    "options": {"summary": {"collapsible": False}},
                }
            }
        )
    )
    return schema


@pytest.fixture
def placeholder_renderer(option_label_from_value_schema):
    answer_store = AnswerStore(
        [
            {"answer_id": "mandatory-radio-answer", "value": "{body_parts}"},
            {"answer_id": "mandatory-checkbox-answer", "value": ["Body"]},
        ]
    )
    renderer = PlaceholderRenderer(
        language="en",
        answer_store=answer_store,
        list_store=ListStore(),
        metadata=ImmutableDict({"trad_as": "ESSENTIAL SERVICES LTD"}),
        response_metadata={},
        schema=option_label_from_value_schema,
    )
    return renderer


@pytest.fixture
def mock_renderer(mock_schema):
    return PlaceholderRenderer(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata=ImmutableDict({}),
        response_metadata={},
        schema=mock_schema,
    )


@pytest.fixture
def option_label_from_value_schema():
    return load_schema_from_name("test_placeholder_option_label_from_value", "en")


@pytest.fixture
def default_placeholder_value_schema():
    return load_schema_from_name("test_placeholder_default_value", "en")


@pytest.fixture
def transformer(mock_renderer, mock_schema):
    def _transform(language="en"):
        return PlaceholderTransforms(
            language=language, schema=mock_schema, renderer=mock_renderer
        )

    return _transform


@pytest.fixture
@pytest.mark.usefixtures("app", "gb_locale")
def question_json():
    return {
        "id": "confirm-date-of-birth-proxy",
        "title": "Confirm date of birth",
        "type": "General",
        "answers": [
            {
                "id": "confirm-date-of-birth-answer-proxy",
                "mandatory": True,
                "options": [
                    {
                        "label": {
                            "text": "{person_name_possessive} age is {age}. Is this correct?",
                            "placeholders": [
                                {
                                    "placeholder": "person_name_possessive",
                                    "transforms": [
                                        {
                                            "arguments": {
                                                "delimiter": " ",
                                                "list_to_concatenate": [
                                                    {
                                                        "source": "answers",
                                                        "identifier": "first-name",
                                                    },
                                                    {
                                                        "source": "answers",
                                                        "identifier": "last-name",
                                                    },
                                                ],
                                            },
                                            "transform": "concatenate_list",
                                        },
                                        {
                                            "arguments": {
                                                "string_to_format": {
                                                    "source": "previous_transform"
                                                }
                                            },
                                            "transform": "format_possessive",
                                        },
                                    ],
                                },
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
                                                "second_date": {"value": "now"},
                                            },
                                        }
                                    ],
                                },
                            ],
                        },
                        "value": "Yes",
                    },
                    {
                        "label": "No, I need to change their date of birth",
                        "value": "No",
                    },
                ],
                "type": "Radio",
            }
        ],
    }


@pytest.fixture
def pointers(question_json):
    return list(find_pointers_containing(question_json, "placeholders"))


@pytest.fixture
def mock_list_store():
    serialized = [
        {
            "name": "people",
            "primary_person": "abcdef",
            "items": ["abcdef", "ghijkl", "xyzabc"],
        },
        {"name": "pets", "items": ["tuvwxy"]},
    ]

    return ListStore.deserialize(serialized)


@pytest.fixture
def mock_location():
    return Location(section_id="section-foo", block_id="block-bar")


@pytest.fixture
def schema(mocker):
    return mocker.MagicMock(spec=QuestionnaireSchema)


@pytest.fixture
def mock_answer_store(mocker):
    return mocker.MagicMock(spec=AnswerStore)


@pytest.fixture
def progress_store(mocker):
    _progress_store = mocker.MagicMock(spec=ProgressStore)
    _progress_store.locations = []
    return _progress_store


@pytest.fixture
def list_store(mocker):
    return mocker.MagicMock(spec=ListStore)


@pytest.fixture
def questionnaire_store(mock_list_store, mock_answer_store, progress_store, mocker):
    return mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_answer_store,
        list_store=mock_list_store,
        progress_store=progress_store,
    )


@pytest.fixture
def metadata(mocker):
    return mocker.MagicMock()


@pytest.fixture
def block_ids():
    return ["block-a", "block-b", "block-c", "block-b", "block-c"]


@pytest.fixture
def section_id():
    return "section-1"


@pytest.fixture
def list_item_id():
    return "list_item_id"


@pytest.fixture
def list_name():
    return "list_name"


@pytest.fixture
def routing_path(block_ids, section_id, list_item_id, list_name):
    return RoutingPath(
        block_ids,
        section_id=section_id,
        list_item_id=list_item_id,
        list_name=list_name,
    )


@pytest.fixture
def answers():
    return {
        "low": Answer(answer_id="low", value=1),
        "medium": Answer(answer_id="medium", value=5),
        "high": Answer(answer_id="high", value=10),
        "list_answer": Answer(answer_id="list_answer", value=["a", "abc", "cba"]),
        "other_list_answer": Answer(
            answer_id="other_list_answer", value=["x", "y", "z"]
        ),
        "other_list_answer_2": Answer(
            answer_id="other_list_answer_2", value=["a", "abc", "cba"]
        ),
        "text_answer": Answer(answer_id="small_string", value="abc"),
        "other_text_answer": Answer(answer_id="other_string", value="xyz"),
        "missing_answer": Answer(answer_id="missing", value=1),
    }


@pytest.fixture
def current_location():
    return Location(section_id="some-section", block_id="some-block")


@pytest.fixture
def questionnaire_schema():
    return QuestionnaireSchema(
        {
            "questionnaire_flow": {
                "type": "Linear",
                "options": {"summary": {"collapsible": False}},
            }
        }
    )


@pytest.fixture
def questionnaire_store_get_relationship_collectors_by_list_name_patch(mocker):
    patch_method = "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdater._get_relationship_collectors_by_list_name"
    patched = mocker.patch(patch_method)
    patched.return_value = None
