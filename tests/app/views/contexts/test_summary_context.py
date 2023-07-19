import pytest
from markupsafe import Markup

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.utilities.schema import load_schema_from_name
from app.views.contexts.summary_context import SummaryContext


@pytest.mark.usefixtures("app")
def test_context_for_summary():
    schema = load_schema_from_name("test_view_submitted_response_repeating_sections")

    list_store = ListStore(
        [{"items": ["jufPpX", "fjWZET"], "name": "people", "primary_person": "jufPpX"}]
    )

    answer_store = AnswerStore(
        [
            {"answer_id": "name-answer", "value": "John"},
            {"answer_id": "address-answer", "value": "1 Street"},
            {"answer_id": "you-live-here", "value": "Yes"},
            {"answer_id": "first-name", "value": "James", "list_item_id": "jufPpX"},
            {"answer_id": "last-name", "value": "Bond", "list_item_id": "jufPpX"},
            {"answer_id": "first-name", "value": "Jane", "list_item_id": "fjWZET"},
            {"answer_id": "last-name", "value": "Doe", "list_item_id": "fjWZET"},
            {"answer_id": "anyone-else", "value": "No"},
            {"answer_id": "skip-first-block-answer", "value": "Yes"},
            {"answer_id": "second-number-answer-also-in-total", "value": 1},
            {"answer_id": "third-number-answer", "value": 2, "list_item_id": "jufPpX"},
            {
                "answer_id": "third-number-answer-also-in-total",
                "value": 2,
                "list_item_id": "jufPpX",
            },
            {
                "answer_id": "checkbox-answer",
                "value": ["{calc_value_2}"],
                "list_item_id": "jufPpX",
            },
            {"answer_id": "third-number-answer", "value": 1, "list_item_id": "fjWZET"},
            {
                "answer_id": "third-number-answer-also-in-total",
                "value": 1,
                "list_item_id": "fjWZET",
            },
            {
                "answer_id": "checkbox-answer",
                "value": ["{calc_value_1}"],
                "list_item_id": "fjWZET",
            },
        ]
    )

    progress_store = ProgressStore(
        [
            {
                "section_id": "name-section",
                "block_ids": ["name", "address"],
                "status": "COMPLETED",
            },
            {
                "section_id": "section",
                "block_ids": ["primary-person-list-collector", "list-collector"],
                "status": "COMPLETED",
            },
            {
                "section_id": "questions-section",
                "block_ids": [
                    "skip-first-block",
                    "second-number-block",
                    "currency-total-playback-1",
                ],
                "status": "COMPLETED",
            },
            {
                "section_id": "calculated-summary-section",
                "block_ids": [
                    "third-number-block",
                    "currency-total-playback-2",
                    "mutually-exclusive-checkbox",
                ],
                "status": "COMPLETED",
                "list_item_id": "jufPpX",
            },
            {
                "section_id": "calculated-summary-section",
                "block_ids": [
                    "third-number-block",
                    "currency-total-playback-2",
                    "mutually-exclusive-checkbox",
                ],
                "status": "COMPLETED",
                "list_item_id": "fjWZET",
            },
        ]
    )

    summary_context = SummaryContext(
        language=DEFAULT_LANGUAGE_CODE,
        schema=schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        metadata=None,
        response_metadata={},
        view_submitted_response=False,
    )
    context = summary_context()
    expected = {
        "answers_are_editable": False,
        "collapsible": False,
        "sections": [
            {
                "groups": [
                    {
                        "blocks": [
                            {
                                "id": "name",
                                "number": None,
                                "question": {
                                    "answers": [
                                        {
                                            "currency": None,
                                            "id": "name-answer",
                                            "label": "Full name",
                                            "link": "/questionnaire/name/#name-answer",
                                            "type": "textfield",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": Markup("John"),
                                        }
                                    ],
                                    "id": "name-question",
                                    "number": None,
                                    "title": "What is your name?",
                                    "type": "General",
                                },
                                "title": None,
                            }
                        ],
                        "id": "personal-details-group-0",
                        "links": {},
                        "placeholder_text": None,
                        "title": "Personal Details",
                    },
                    {
                        "blocks": [
                            {
                                "id": "address",
                                "number": None,
                                "question": {
                                    "answers": [
                                        {
                                            "currency": None,
                                            "id": "address-answer",
                                            "label": "Postcode",
                                            "link": "/questionnaire/address/#address-answer",
                                            "type": "textfield",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": Markup("1 Street"),
                                        }
                                    ],
                                    "id": "address-question",
                                    "number": None,
                                    "title": "What is your address?",
                                    "type": "General",
                                },
                                "title": None,
                            }
                        ],
                        "id": "address-details-group-0",
                        "links": {},
                        "placeholder_text": None,
                        "title": "Address Details",
                    },
                ],
                "title": "Personal Details Section",
            },
            {
                "groups": [
                    {
                        "blocks": [
                            {
                                "id": "skip-first-block",
                                "number": None,
                                "question": {
                                    "answers": [
                                        {
                                            "currency": None,
                                            "id": "skip-first-block-answer",
                                            "label": None,
                                            "link": "/questionnaire/skip-first-block/#skip-first-block-answer",
                                            "type": "radio",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": {
                                                "detail_answer_value": None,
                                                "label": "Yes",
                                            },
                                        }
                                    ],
                                    "id": "skip-first-block-question",
                                    "number": None,
                                    "title": "Skip First Block so it doesn’t appear in Total?",
                                    "type": "General",
                                },
                                "title": None,
                            },
                            {
                                "id": "second-number-block",
                                "number": None,
                                "question": {
                                    "answers": [
                                        {
                                            "currency": "GBP",
                                            "id": "second-number-answer-also-in-total",
                                            "label": "Second answer label also in total (optional)",
                                            "link": "/questionnaire/second-number-block/#second-number-answer-also-in-total",
                                            "type": "currency",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": 1,
                                        }
                                    ],
                                    "id": "second-number-question-also-in-total",
                                    "number": None,
                                    "title": "Second Number Additional Question Title",
                                    "type": "General",
                                },
                                "title": None,
                            },
                        ],
                        "id": "radio-0",
                        "links": {},
                        "placeholder_text": None,
                        "title": "Questions Group",
                    }
                ],
                "title": "Questions Section",
            },
            {
                "groups": [
                    {
                        "blocks": [
                            {
                                "id": "third-number-block",
                                "number": None,
                                "question": {
                                    "answers": [
                                        {
                                            "currency": "GBP",
                                            "id": "third-number-answer",
                                            "label": "Third answer in currency label",
                                            "link": "/questionnaire/people/jufPpX/third-number-block/#third-number-answer",
                                            "type": "currency",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": 2,
                                        },
                                        {
                                            "currency": "GBP",
                                            "id": "third-number-answer-also-in-total",
                                            "label": "Third answer label also in currency total (optional)",
                                            "link": "/questionnaire/people/jufPpX/third-number-block/#third-number-answer-also-in-total",
                                            "type": "currency",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": 2,
                                        },
                                    ],
                                    "id": "third-number-question",
                                    "number": None,
                                    "title": "Third Number Question Title",
                                    "type": "General",
                                },
                                "title": None,
                            },
                            {
                                "id": "mutually-exclusive-checkbox",
                                "number": None,
                                "question": {
                                    "answers": [
                                        {
                                            "currency": None,
                                            "id": "checkbox-answer",
                                            "label": None,
                                            "link": "/questionnaire/people/jufPpX/mutually-exclusive-checkbox/#checkbox-answer",
                                            "type": "checkbox",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": [
                                                {
                                                    "detail_answer_value": None,
                                                    "label": "4 - calculated summary answer (current section)",
                                                }
                                            ],
                                        }
                                    ],
                                    "id": "mutually-exclusive-checkbox-question",
                                    "number": None,
                                    "title": "Which answer did you give to question 4 and a half?",
                                    "type": "MutuallyExclusive",
                                },
                                "title": None,
                            },
                            {
                                "id": "skippable-block",
                                "number": None,
                                "question": {
                                    "answers": [
                                        {
                                            "currency": "GBP",
                                            "id": "skippable-answer",
                                            "label": "Capital expenditure",
                                            "link": "/questionnaire/people/jufPpX/skippable-block/#skippable-answer",
                                            "type": "currency",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": None,
                                        }
                                    ],
                                    "id": "skippable-question",
                                    "number": None,
                                    "title": "How much did James Bond spend on fruit?",
                                    "type": "General",
                                },
                                "title": None,
                            },
                        ],
                        "id": "calculated-summary-0",
                        "links": {},
                        "placeholder_text": None,
                        "title": "Calculated Summary Group",
                    }
                ],
                "title": "James Bond",
            },
            {
                "groups": [
                    {
                        "blocks": [
                            {
                                "id": "third-number-block",
                                "number": None,
                                "question": {
                                    "answers": [
                                        {
                                            "currency": "GBP",
                                            "id": "third-number-answer",
                                            "label": "Third answer in currency label",
                                            "link": "/questionnaire/people/fjWZET/third-number-block/#third-number-answer",
                                            "type": "currency",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": 1,
                                        },
                                        {
                                            "currency": "GBP",
                                            "id": "third-number-answer-also-in-total",
                                            "label": "Third answer label also in currency total (optional)",
                                            "link": "/questionnaire/people/fjWZET/third-number-block/#third-number-answer-also-in-total",
                                            "type": "currency",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": 1,
                                        },
                                    ],
                                    "id": "third-number-question",
                                    "number": None,
                                    "title": "Third Number Question Title",
                                    "type": "General",
                                },
                                "title": None,
                            },
                            {
                                "id": "mutually-exclusive-checkbox",
                                "number": None,
                                "question": {
                                    "answers": [
                                        {
                                            "currency": None,
                                            "id": "checkbox-answer",
                                            "label": None,
                                            "link": "/questionnaire/people/fjWZET/mutually-exclusive-checkbox/#checkbox-answer",
                                            "type": "checkbox",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": [
                                                {
                                                    "detail_answer_value": None,
                                                    "label": "1 - calculated summary answer (previous section)",
                                                }
                                            ],
                                        }
                                    ],
                                    "id": "mutually-exclusive-checkbox-question",
                                    "number": None,
                                    "title": "Which answer did you give to question 4 and a half?",
                                    "type": "MutuallyExclusive",
                                },
                                "title": None,
                            },
                            {
                                "id": "skippable-block",
                                "number": None,
                                "question": {
                                    "answers": [
                                        {
                                            "currency": "GBP",
                                            "id": "skippable-answer",
                                            "label": "Capital expenditure",
                                            "link": "/questionnaire/people/fjWZET/skippable-block/#skippable-answer",
                                            "type": "currency",
                                            "unit": None,
                                            "unit_length": None,
                                            "value": None,
                                        }
                                    ],
                                    "id": "skippable-question",
                                    "number": None,
                                    "title": "How much did Jane Doe spend on fruit?",
                                    "type": "General",
                                },
                                "title": None,
                            },
                        ],
                        "id": "calculated-summary-0-1",
                        "links": {},
                        "placeholder_text": None,
                        "title": "Calculated Summary Group",
                    }
                ],
                "title": "Jane Doe",
            },
        ],
        "summary_type": "Summary",
        "view_submitted_response": False,
    }
    assert context == expected
