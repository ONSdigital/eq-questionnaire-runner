import pytest
from flask_babel import lazy_gettext

from app.questionnaire import QuestionnaireSchema
from app.views.contexts.preview_context import (
    PreviewContext,
    PreviewNotEnabledException,
)
from tests.app.views.contexts import assert_preview_context


def test_build_preview_rendering_context(
    test_introduction_preview_linear_schema,
    answer_store,
    list_store,
    progress_store,
    questionnaire_store,
):
    preview_context = PreviewContext(
        "en",
        test_introduction_preview_linear_schema,
        answer_store,
        list_store,
        progress_store,
        metadata=questionnaire_store.metadata,
        response_metadata=questionnaire_store.response_metadata,
    )

    preview_context = preview_context()

    assert_preview_context(preview_context)


def test_build_preview_context(
    test_introduction_preview_linear_schema,
    answer_store,
    list_store,
    progress_store,
    questionnaire_store,
):
    preview_context = PreviewContext(
        "en",
        test_introduction_preview_linear_schema,
        answer_store,
        list_store,
        progress_store,
        metadata=questionnaire_store.metadata,
        response_metadata=questionnaire_store.response_metadata,
    )
    context = preview_context()

    expected_context = {
        "groups": [
            {
                "blocks": [
                    {
                        "question": {
                            "answers": [
                                {
                                    "description": "Select your answer",
                                    "guidance": {
                                        "contents": [
                                            {
                                                "description": "You can only pick one answer"
                                            }
                                        ],
                                        "hide_guidance": "Show more information",
                                        "show_guidance": "Show more information",
                                    },
                                    "options": ["Yes", "No"],
                                    "options_text": lazy_gettext(
                                        "You can answer with one of the following options:"
                                    ),
                                }
                            ],
                            "descriptions": [
                                "<p>Your return should relate to the calendar year 2021.</p>"
                            ],
                            "guidance": {
                                "contents": [
                                    {
                                        "description": "Please provide figures for the period in which you were trading."
                                    }
                                ]
                            },
                            "id": "report-radio",
                            "title": "Are you able to report for the calendar month 2 February 2016 to 3 March 2016?",
                            "type": "General",
                        }
                    },
                    {
                        "question": {
                            "answers": [{"label": "Start date"}],
                            "descriptions": None,
                            "guidance": None,
                            "id": "start-date",
                            "title": "Please provide optional start date",
                            "type": "General",
                        }
                    },
                    {
                        "question": {
                            "answers": [{"label": "End date"}],
                            "descriptions": None,
                            "guidance": None,
                            "id": "end-date",
                            "title": "Please provide optional end date",
                            "type": "General",
                        }
                    },
                    {
                        "question": {
                            "answers": [
                                {
                                    "options": ["Yes", "No"],
                                    "options_text": lazy_gettext(
                                        "You can answer with one of the following options:"
                                    ),
                                }
                            ],
                            "descriptions": [
                                "<p>Your return should relate to the calendar year 2021.</p>"
                            ],
                            "guidance": None,
                            "id": "report-radio-second",
                            "title": "Are you sure you are able to report for the calendar month ref_p_start_date to ref_p_end_date?",
                            "type": "General",
                        }
                    },
                    {
                        "question": {
                            "answers": [
                                {
                                    "options": [
                                        "Public sector projects",
                                        "Private sector projects",
                                    ],
                                    "options_text": lazy_gettext(
                                        "You can answer with the following options:"
                                    ),
                                }
                            ],
                            "descriptions": None,
                            "guidance": {
                                "contents": [
                                    {"description": "<strong>Include:</strong>"},
                                    {
                                        "list": [
                                            "Local public authorities and agencies",
                                            "Regional and national authorities and agencies",
                                        ]
                                    },
                                ]
                            },
                            "id": "projects-checkbox",
                            "title": "Which sector did ESSENTIAL "
                            "ENTERPRISE LTD. carry out work "
                            "for?",
                            "type": "General",
                        }
                    },
                    {
                        "question": {
                            "answers": [{"label": "Total turnover"}],
                            "descriptions": None,
                            "guidance": {
                                "contents": [
                                    {"description": "<strong>Include:</strong>"},
                                    {
                                        "list": [
                                            "exports",
                                            "payments for work in progress",
                                            "costs incurred and passed on to customers",
                                            "income from sub-contracted activities",
                                            "commission",
                                            "sales of goods purchased for resale",
                                            "revenue earned from other parts of the business not named, please supply at fair value",
                                        ]
                                    },
                                    {"description": "<strong>Exclude:</strong>"},
                                    {
                                        "list": [
                                            "VAT",
                                            "income from the sale of fixed capital assets",
                                            "grants and subsidies",
                                            "insurance claims",
                                            "interest received",
                                        ]
                                    },
                                ]
                            },
                            "id": "turnover-variants-block",
                            "title": "What was your total turnover",
                            "type": "General",
                        }
                    },
                    {
                        "question": {
                            "answers": [
                                {
                                    "options": [
                                        "68 Abingdon Road, Goathill",
                                        "7 Evelyn Street, Barry",
                                        "251 Argae Lane, Barry",
                                    ],
                                    "options_text": lazy_gettext(
                                        "You can answer with the following options:"
                                    ),
                                },
                                {
                                    "options": ["I prefer not to say"],
                                    "options_text": lazy_gettext(
                                        "You can answer with the following options:"
                                    ),
                                },
                            ],
                            "descriptions": None,
                            "guidance": None,
                            "id": "address-mutually-exclusive-checkbox",
                            "title": "Were your company based at any of the following addresses?",
                            "type": "MutuallyExclusive",
                        }
                    },
                    {
                        "question": {
                            "answers": [
                                {
                                    "label": "Comments",
                                    "max_length": 2000,
                                }
                            ],
                            "descriptions": [
                                "<p>Answer for ESSENTIAL ENTERPRISE LTD.</p>"
                            ],
                            "guidance": None,
                            "id": "further-details-text-area",
                            "title": "Please provide any further details",
                            "type": "General",
                        }
                    },
                ],
                "title": "Main section",
            }
        ]
    }
    assert "groups" in context
    assert_preview_context(context)
    assert len(context["groups"][0]) == 2
    assert "blocks" in context["groups"][0]
    assert context == expected_context


def test_preview_questions_disabled_raises_exception(
    answer_store,
    list_store,
    progress_store,
    questionnaire_store,
):
    schema = QuestionnaireSchema({"preview_questions": False})
    with pytest.raises(PreviewNotEnabledException):
        PreviewContext(
            "en",
            schema,
            answer_store,
            list_store,
            progress_store,
            metadata=questionnaire_store.metadata,
            response_metadata=questionnaire_store.response_metadata,
        )
