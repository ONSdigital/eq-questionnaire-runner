# pylint: disable=redefined-outer-name, too-many-lines

import pytest

from app.data_models import QuestionnaireStore
from app.data_models.answer_store import Answer, AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.progress_store import CompletionStatus, ProgressStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import Location
from app.questionnaire.placeholder_parser import PlaceholderParser
from app.questionnaire.placeholder_renderer import (
    PlaceholderRenderer,
    find_pointers_containing,
)
from app.questionnaire.placeholder_transforms import PlaceholderTransforms
from app.questionnaire.router import Router
from app.questionnaire.routing_path import RoutingPath
from app.utilities.schema import load_schema_from_name


def get_metadata(extra_metadata: dict = None):
    extra_metadata = extra_metadata or {}
    metadata = {
        "response_id": "1",
        "account_service_url": "account_service_url",
        "tx_id": "tx_id",
        "collection_exercise_sid": "collection_exercise_sid",
        "case_id": "case_id",
        **extra_metadata,
    }
    return MetadataProxy.from_dict(metadata)


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
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        location=location,
        renderer=mock_renderer,
        progress_store=ProgressStore(),
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
                                "type": "Question",
                                "id": "when",
                                "question": {
                                    "type": "General",
                                    "id": "when-question",
                                    "title": "when answer title",
                                    "answers": [
                                        {
                                            "type": "Radio",
                                            "id": "when-answer",
                                            "mandatory": True,
                                            "options": [
                                                {"label": "Yes", "value": "Yes"},
                                                {"label": "No", "value": "No"},
                                            ],
                                        }
                                    ],
                                },
                            },
                            {
                                "id": "block1",
                                "type": "Question",
                                "title": "Block 1",
                                "question_variants": [
                                    {
                                        "when": {
                                            "==": [
                                                {
                                                    "identifier": "when-answer",
                                                    "source": "answers",
                                                },
                                                "yes",
                                            ]
                                        },
                                        "question": {
                                            "id": "question1",
                                            "type": "General",
                                            "title": "Question 1, Yes",
                                            "answers": [
                                                {
                                                    "id": "answer1",
                                                    "label": "Answer 1 Variant 1",
                                                    "type": "General",
                                                }
                                            ],
                                        },
                                    },
                                    {
                                        "when": {
                                            "!=": [
                                                {
                                                    "identifier": "when-answer",
                                                    "source": "answers",
                                                },
                                                "yes",
                                            ]
                                        },
                                        "question": {
                                            "id": "question1",
                                            "type": "General",
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
                            },
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
                                    "type": "General",
                                    "title": "Question 1",
                                    "answers": [
                                        {
                                            "id": "answer1",
                                            "label": "Answer 1",
                                            "type": "General",
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
                                "type": "Question",
                                "id": "when",
                                "question": {
                                    "type": "General",
                                    "id": "when-question",
                                    "title": "when answer title",
                                    "answers": [
                                        {
                                            "type": "Radio",
                                            "id": "when-answer",
                                            "mandatory": True,
                                            "options": [
                                                {"label": "Yes", "value": "Yes"},
                                                {"label": "No", "value": "No"},
                                            ],
                                        }
                                    ],
                                },
                            },
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
                                                    "type": "General",
                                                    "action": {
                                                        "type": "RedirectToListAddBlock"
                                                    },
                                                }
                                            ],
                                        },
                                        "when": {
                                            "==": [
                                                {
                                                    "identifier": "when-answer",
                                                    "source": "answers",
                                                },
                                                "yes",
                                            ]
                                        },
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
                                        "when": {
                                            "==": [
                                                {
                                                    "identifier": "when-answer",
                                                    "source": "answers",
                                                },
                                                "no",
                                            ]
                                        },
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
                                            "when": {
                                                "==": [
                                                    {
                                                        "identifier": "when-answer",
                                                        "source": "answers",
                                                    },
                                                    "yes",
                                                ]
                                            },
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
                                            "when": {
                                                "==": [
                                                    {
                                                        "identifier": "when-answer",
                                                        "source": "answers",
                                                    },
                                                    "no",
                                                ]
                                            },
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
                                            "when": {
                                                "==": [
                                                    {
                                                        "identifier": "when-answer",
                                                        "source": "answers",
                                                    },
                                                    "yes",
                                                ]
                                            },
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
                                            "when": {
                                                "==": [
                                                    {
                                                        "identifier": "when-answer",
                                                        "source": "answers",
                                                    },
                                                    "no",
                                                ]
                                            },
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
                                            "when": {
                                                "==": [
                                                    {
                                                        "identifier": "when-answer",
                                                        "source": "answers",
                                                    },
                                                    "yes",
                                                ]
                                            },
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
                                            "when": {
                                                "==": [
                                                    {
                                                        "identifier": "when-answer",
                                                        "source": "answers",
                                                    },
                                                    "no",
                                                ]
                                            },
                                        },
                                    ],
                                },
                            },
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
                                                {
                                                    "count": [
                                                        {
                                                            "source": "list",
                                                            "identifier": "list",
                                                        }
                                                    ]
                                                },
                                                0,
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
                                        {
                                            "count": [
                                                {
                                                    "source": "list",
                                                    "identifier": "list",
                                                }
                                            ]
                                        },
                                        0,
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
                                "when": {
                                    "<": [
                                        0,
                                        {
                                            "identifier": "not-the-list",
                                            "source": "list",
                                            "selector": "count",
                                        },
                                    ]
                                },
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
                                "when": {
                                    ">": [
                                        {
                                            "identifier": "list",
                                            "source": "list",
                                            "selector": "count",
                                        },
                                        0,
                                    ]
                                },
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
                                            "identifier": "missing-the-source-attribute",
                                            "selector": "count",
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
                                "type": "Question",
                                "id": "age",
                                "question": {
                                    "type": "General",
                                    "id": "age-question",
                                    "title": "when answer title",
                                    "answers": [
                                        {
                                            "id": "age-answer",
                                            "type": "Unit",
                                            "label": "Your age",
                                            "mandatory": True,
                                        }
                                    ],
                                },
                            },
                            {
                                "id": "block1",
                                "type": "Question",
                                "title": "Block 1",
                                "content_variants": [
                                    {
                                        "content": {"title": "You are over 16"},
                                        "when": {
                                            ">": [
                                                {
                                                    "identifier": "age-answer",
                                                    "source": "answers",
                                                },
                                                16,
                                            ]
                                        },
                                    },
                                    {
                                        "content": {"title": "You are under 16"},
                                        "when": {
                                            "<=": [
                                                {
                                                    "identifier": "age-answer",
                                                    "source": "answers",
                                                },
                                                16,
                                            ]
                                        },
                                    },
                                    {
                                        "content": {"title": "You are ageless"},
                                        "when": {
                                            "==": [
                                                {
                                                    "identifier": "age-answer",
                                                    "source": "answers",
                                                },
                                                None,
                                            ]
                                        },
                                    },
                                ],
                            },
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
                                    "type": "General",
                                    "answers": [
                                        {
                                            "id": "answer1",
                                            "label": "Answer 1",
                                            "type": "General",
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
def mock_schema(mocker):
    schema = mocker.MagicMock(
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
        metadata=get_metadata({"trad_as": "ESSENTIAL SERVICES LTD"}),
        response_metadata={},
        schema=option_label_from_value_schema,
        progress_store=ProgressStore(),
        location=Location(section_id="checkbox-section"),
    )
    return renderer


@pytest.fixture
def mock_renderer(mock_schema):
    return PlaceholderRenderer(
        language="en",
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata=get_metadata(),
        response_metadata={},
        schema=mock_schema,
        progress_store=ProgressStore(),
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
def placholder_transform_question_json():
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
def placholder_transform_pointers(placholder_transform_question_json):
    return list(
        find_pointers_containing(placholder_transform_question_json, "placeholders")
    )


@pytest.fixture
def populated_list_store():
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
def mock_empty_schema(mocker):
    return mocker.MagicMock(spec=QuestionnaireSchema)


@pytest.fixture
def mock_empty_answer_store(mocker):
    return mocker.MagicMock(spec=AnswerStore)


@pytest.fixture
def mock_router(mocker):
    return mocker.MagicMock(spec=Router)


@pytest.fixture
def mock_empty_progress_store(mocker):
    progress_store = mocker.MagicMock(spec=ProgressStore)
    progress_store.locations = []
    return progress_store


@pytest.fixture
def mock_questionnaire_store(
    populated_list_store, mock_empty_answer_store, mock_empty_progress_store, mocker
):
    return mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_empty_answer_store,
        list_store=populated_list_store,
        progress_store=mock_empty_progress_store,
    )


@pytest.fixture
def block_ids():
    return ["block-a", "block-b", "block-c", "block-b", "block-c"]


@pytest.fixture
def routing_path(block_ids):
    return RoutingPath(
        block_ids,
        section_id="section-1",
        list_item_id="list_item_id",
        list_name="list_name",
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


@pytest.fixture
def calculated_question_with_dependent_sections_schema_non_repeating():
    return load_schema_from_name(
        "test_validation_sum_against_total_hub_with_dependent_section"
    )


@pytest.fixture
def calculated_question_with_dependent_sections_schema_repeating():
    return load_schema_from_name(
        "test_validation_sum_against_total_repeating_with_dependent_section"
    )


@pytest.fixture
def calculated_question_with_dependent_sections_schema():
    return load_schema_from_name("test_validation_sum_against_value_source")


@pytest.fixture
def calculated_summary_schema():
    return load_schema_from_name("test_calculated_summary")


@pytest.fixture
def numbers_schema():
    return load_schema_from_name("test_numbers")


@pytest.fixture
def dynamic_radio_options_from_checkbox_schema():
    return load_schema_from_name("test_dynamic_radio_options_from_checkbox")


@pytest.fixture
def dynamic_answer_options_function_driven_schema():
    return load_schema_from_name("test_dynamic_answer_options_function_driven")


@pytest.fixture
def skipping_section_dependencies_schema():
    return load_schema_from_name("test_routing_and_skipping_section_dependencies")


@pytest.fixture
def section_dependencies_calculated_summary_schema():
    return load_schema_from_name(
        "test_routing_and_skipping_section_dependencies_calculated_summary"
    )


@pytest.fixture
def section_dependencies_new_calculated_summary_schema():
    return load_schema_from_name(
        "test_routing_and_skipping_section_dependencies_new_calculated_summary"
    )


@pytest.fixture
def progress_block_dependencies_schema():
    return load_schema_from_name("test_progress_value_source_calculated_summary")


@pytest.fixture
def progress_section_dependencies_schema():
    return load_schema_from_name(
        "test_progress_value_source_section_enabled_hub_complex"
    )


@pytest.fixture
def progress_dependencies_schema():
    return load_schema_from_name(
        "test_progress_value_source_calculated_summary_extended"
    )


@pytest.fixture
def grand_calculated_summary_schema():
    return load_schema_from_name("test_grand_calculated_summary")


@pytest.fixture
def grand_calculated_summary_progress_store():
    return ProgressStore(
        [
            {
                "section_id": "section-1",
                "block_ids": [
                    "first-number-block",
                    "second-number-block",
                    "distance-calculated-summary-1",
                    "number-calculated-summary-1",
                ],
                "status": CompletionStatus.COMPLETED,
            }
        ]
    )


@pytest.fixture
@pytest.mark.usefixtures("app", "gb_locale")
def placeholder_transform_question_dynamic_answers_json():
    return {
        "dynamic_answers": {
            "values": {"source": "list", "identifier": "supermarkets"},
            "answers": [
                {
                    "label": {
                        "text": "Percentage of shopping at {transformed_value}",
                        "placeholders": [
                            {
                                "placeholder": "transformed_value",
                                "value": {
                                    "source": "answers",
                                    "identifier": "supermarket-name",
                                },
                            }
                        ],
                    },
                    "id": "percentage-of-shopping",
                    "mandatory": False,
                    "type": "Percentage",
                    "maximum": {"value": 100},
                    "decimal_places": 0,
                }
            ],
        },
        "answers": [],
        "id": "dynamic-answer-question",
        "title": "What percent of your shopping do you do at each of the following supermarket?",
        "type": "General",
    }


@pytest.fixture
@pytest.mark.usefixtures("app", "gb_locale")
def placeholder_transform_question_dynamic_answers_pointer_json():
    return {
        "question": {
            "dynamic_answers": {
                "values": {"source": "list", "identifier": "supermarkets"},
                "answers": [
                    {
                        "label": {
                            "text": "Percentage of shopping at {transformed_value}",
                            "placeholders": [
                                {
                                    "placeholder": "transformed_value",
                                    "value": {
                                        "source": "answers",
                                        "identifier": "supermarket-name",
                                    },
                                }
                            ],
                        },
                        "id": "percentage-of-shopping",
                        "mandatory": False,
                        "type": "Percentage",
                        "maximum": {"value": 100},
                        "decimal_places": 0,
                    }
                ],
            },
            "answers": [],
            "id": "dynamic-answer-question",
            "title": "What percent of your shopping do you do at each of the following supermarket?",
            "type": "General",
        }
    }
