# pylint: disable=redefined-outer-name
from unittest.mock import Mock

import pytest
from werkzeug.datastructures import ImmutableDict

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import Location
from app.questionnaire.placeholder_parser import PlaceholderParser
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.placeholder_transforms import PlaceholderTransforms


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
def labels_schema_with_placeholders():
    return {
        "sections": [
            {
                "id": "checkbox-section",
                "groups": [
                    {
                        "blocks": [
                            {
                                "type": "Question",
                                "id": "mandatory-checkbox",
                                "question": {
                                    "answers": [
                                        {
                                            "id": "mandatory-checkbox-answer",
                                            "mandatory": True,
                                            "options": [
                                                {"label": "Head", "value": "Head"},
                                                {
                                                    "label": "Body",
                                                    "value": "Body",
                                                    "q_code": "1",
                                                },
                                                {
                                                    "label": "Right Arm",
                                                    "value": "Right Arm",
                                                    "q_code": "2",
                                                },
                                                {
                                                    "label": "Left Arm",
                                                    "value": "Left Arm",
                                                    "q_code": "3",
                                                },
                                            ],
                                            "type": "Checkbox",
                                        }
                                    ],
                                    "id": "mandatory-checkbox-question",
                                    "title": "When you had your accident, where did you sustain injuries?",
                                    "type": "General",
                                },
                            },
                            {
                                "type": "Question",
                                "id": "recovery-question-checkbox-block",
                                "question": {
                                    "id": "recovery-question-checkbox",
                                    "title": {
                                        "text": "How long did it take to recover from the injury to your {body_part}?",
                                        "placeholders": [
                                            {
                                                "placeholder": "body_part",
                                                "transforms": [
                                                    {
                                                        "transform": "first_non_empty_item",
                                                        "arguments": {
                                                            "items": [
                                                                {
                                                                    "source": "answers",
                                                                    "identifier": "mandatory-checkbox-answer",
                                                                }
                                                            ]
                                                        },
                                                    },
                                                    {
                                                        "transform": "option_label_from_value",
                                                        "arguments": {
                                                            "value": {
                                                                "source": "previous_transform"
                                                            },
                                                            "answer_id": "mandatory-checkbox-answer",
                                                        },
                                                    },
                                                ],
                                            }
                                        ],
                                    },
                                    "type": "General",
                                    "answers": [
                                        {
                                            "id": "recovery-checkbox-answer",
                                            "label": "Recovery time",
                                            "mandatory": False,
                                            "type": "Number",
                                        }
                                    ],
                                },
                                "skip_conditions": {
                                    "when": {
                                        ">": [
                                            {
                                                "count": [
                                                    {
                                                        "identifier": "mandatory-checkbox-answer",
                                                        "source": "answers",
                                                    }
                                                ]
                                            },
                                            1,
                                        ]
                                    }
                                },
                            },
                            {
                                "type": "Question",
                                "id": "mandatory-radio",
                                "question": {
                                    "type": "General",
                                    "id": "mandatory-radio-question",
                                    "title": "If you suffered any one injury from the options below, please select the most serious one.",
                                    "answers": [
                                        {
                                            "type": "Radio",
                                            "id": "mandatory-radio-answer",
                                            "mandatory": True,
                                            "options": [
                                                {
                                                    "label": {
                                                        "text": "{body_part} (piped)",
                                                        "placeholders": [
                                                            {
                                                                "placeholder": "body_part",
                                                                "transforms": [
                                                                    {
                                                                        "transform": "first_non_empty_item",
                                                                        "arguments": {
                                                                            "items": [
                                                                                {
                                                                                    "source": "answers",
                                                                                    "identifier": "mandatory-checkbox-answer",
                                                                                }
                                                                            ]
                                                                        },
                                                                    }
                                                                ],
                                                            }
                                                        ],
                                                    },
                                                    "value": "{body_part}",
                                                },
                                                {"label": "Eyes", "value": "Eyes"},
                                                {"label": "Ears", "value": "Ears"},
                                                {"label": "Mouth", "value": "Mouth"},
                                                {"label": "Nose", "value": "Nose"},
                                            ],
                                        }
                                    ],
                                },
                                "skip_conditions": {
                                    "when": {
                                        "==": [
                                            {
                                                "count": [
                                                    {
                                                        "identifier": "mandatory-checkbox-answer",
                                                        "source": "answers",
                                                    }
                                                ]
                                            },
                                            1,
                                        ]
                                    }
                                },
                            },
                            {
                                "type": "Question",
                                "id": "recovery-question-radio-block",
                                "question": {
                                    "id": "recovery-question-radio",
                                    "title": {
                                        "text": "How long did it take to recover from the injury to your <em>{body_part}</em>?",
                                        "placeholders": [
                                            {
                                                "placeholder": "body_part",
                                                "transforms": [
                                                    {
                                                        "transform": "option_label_from_value",
                                                        "arguments": {
                                                            "value": {
                                                                "source": "answers",
                                                                "identifier": "mandatory-radio-answer",
                                                            },
                                                            "answer_id": "mandatory-radio-answer",
                                                        },
                                                    }
                                                ],
                                            }
                                        ],
                                    },
                                    "type": "General",
                                    "answers": [
                                        {
                                            "id": "recovery-radio-answer",
                                            "label": "Recovery time",
                                            "mandatory": False,
                                            "type": "Number",
                                        }
                                    ],
                                },
                                "skip_conditions": {
                                    "when": {
                                        "==": [
                                            {
                                                "count": [
                                                    {
                                                        "identifier": "mandatory-checkbox-answer",
                                                        "source": "answers",
                                                    }
                                                ]
                                            },
                                            1,
                                        ]
                                    }
                                },
                            },
                        ],
                        "id": "checkboxes",
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
def placeholder_transform(mock_schema, mock_renderer):
    return PlaceholderTransforms(
        language="en", schema=mock_schema, renderer=mock_renderer
    )


@pytest.fixture
def schema_placeholder_renderer(labels_schema_with_placeholders):
    schema = QuestionnaireSchema(labels_schema_with_placeholders)
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
        metadata=ImmutableDict({}),
        response_metadata={},
        schema=schema,
    )
    return schema, renderer


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
def transformer(mock_renderer, mock_schema):
    def _transform(language="en"):
        return PlaceholderTransforms(
            language=language, schema=mock_schema, renderer=mock_renderer
        )

    return _transform
