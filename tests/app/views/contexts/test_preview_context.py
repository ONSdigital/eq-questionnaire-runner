import pytest

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
                                    "description": "Choose Yes or No answer",
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
                                }
                            ],
                            "descriptions": [
                                "<p>Your return should relate to the calendar year 2021.</p>"
                            ],
                            "guidance": None,
                            "id": "report-radio",
                            "instruction": ["Select your answer"],
                            "title": "Are you able to report for the calendar month 2 February 2016 to 3 March 2016?",
                        }
                    },
                    {
                        "question": {
                            "answers": [{"label": "Start date"}],
                            "descriptions": None,
                            "guidance": None,
                            "id": "start-date",
                            "instruction": None,
                            "title": "Please provide optional start date",
                        }
                    },
                    {
                        "question": {
                            "answers": [{"label": "End date"}],
                            "descriptions": None,
                            "guidance": None,
                            "id": "end-date",
                            "instruction": None,
                            "title": "Please provide optional end date",
                        }
                    },
                    {
                        "question": {
                            "answers": [{"options": ["Yes", "No"]}],
                            "descriptions": [
                                "<p>Your return should relate to the calendar year 2021.</p>"
                            ],
                            "guidance": None,
                            "id": "report-radio-second",
                            "instruction": ["Select your answer"],
                            "title": "Are you sure you are able to report for the calendar month ref_p_start_date to ref_p_end_date?",
                        }
                    },
                    {
                        "question": {
                            "answers": [
                                {
                                    "instruction": "Select any answers that apply",
                                    "options": [
                                        "Public sector projects",
                                        "Private sector projects",
                                    ],
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
                            "instruction": None,
                            "title": "Which sector did ESSENTIAL "
                            "ENTERPRISE LTD. carry out work "
                            "for?",
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
                            "instruction": None,
                            "title": "What was your total turnover",
                        }
                    },
                    {
                        "question": {
                            "answers": [
                                {
                                    "instruction": "Select an " "answer",
                                    "options": [
                                        "68 Abingdon Road, Goathill",
                                        "7 Evelyn Street, Barry",
                                        "251 Argae Lane, Barry",
                                    ],
                                },
                                {"options": ["I prefer not to say"]},
                            ],
                            "descriptions": None,
                            "guidance": None,
                            "id": "address-mutually-exclusive-checkbox",
                            "instruction": None,
                            "title": "Were your company based at any of the following addresses?",
                        }
                    },
                    {
                        "question": {
                            "answers": [{"label": "Comments", "max_length": 2000}],
                            "descriptions": [
                                "<p>Answer for ESSENTIAL ENTERPRISE LTD.</p>"
                            ],
                            "guidance": None,
                            "id": "further-details-text-area",
                            "instruction": None,
                            "title": "Please provide any further details",
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
