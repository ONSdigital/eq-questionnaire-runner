from app.views.contexts.preview_context import PreviewContext
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
        questionnaire_store=questionnaire_store,
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
        questionnaire_store=questionnaire_store,
    )
    context = preview_context()

    expected_context = {
        "groups": [
            {
                "title": "Main section",
                "blocks": [
                    {
                        "question": {
                            "id": "report-radio",
                            "title": "Are you able to report for the calendar month 2 February 2016 to 3 March 2016?",
                            "answers": ["Yes", "No"],
                            "descriptions": [
                                "<p>Your return should relate to the calendar year 2021.</p>"
                            ],
                            "guidance": None,
                            "text_length": None,
                            "instruction": ["Select your answer"],
                            "answer_description": "Choose Yes or No answer",
                            "answer_guidance": {
                                "contents": [
                                    {"description": "You can only pick one answer"}
                                ],
                                "hide_guidance": "Show more information",
                                "show_guidance": "Show more information",
                            },
                        },
                    },
                    {
                        "question": {
                            "answer_description": None,
                            "answer_guidance": None,
                            "answers": ["Start date"],
                            "descriptions": None,
                            "guidance": None,
                            "id": "start-date",
                            "instruction": None,
                            "text_length": None,
                            "title": "Please provide optional start date",
                        }
                    },
                    {
                        "question": {
                            "answer_description": None,
                            "answer_guidance": None,
                            "answers": ["End date"],
                            "descriptions": None,
                            "guidance": None,
                            "id": "end-date",
                            "instruction": None,
                            "text_length": None,
                            "title": "Please provide optional end date",
                        }
                    },
                    {
                        "question": {
                            "id": "report-radio-second",
                            "title": "Are you sure you are able to report for the calendar month ref_p_start_date to ref_p_end_date?",
                            "answers": ["Yes", "No"],
                            "descriptions": [
                                "<p>Your return should relate to the calendar year 2021.</p>"
                            ],
                            "guidance": None,
                            "text_length": None,
                            "instruction": ["Select your answer"],
                            "answer_description": None,
                            "answer_guidance": None,
                        },
                    },
                    {
                        "question": {
                            "id": "projects-checkbox",
                            "title": "Which sector did ESSENTIAL ENTERPRISE LTD. carry out work for?",
                            "answers": [
                                "Public sector projects",
                                "Private sector projects",
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
                            "text_length": None,
                            "instruction": None,
                            "answer_description": None,
                            "answer_guidance": None,
                        },
                    },
                    {
                        "question": {
                            "id": "turnover-variants-block",
                            "title": "What was your total turnover",
                            "answers": ["Total turnover"],
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
                            "text_length": None,
                            "instruction": None,
                            "answer_description": None,
                            "answer_guidance": None,
                        },
                    },
                    {
                        "question": {
                            "id": "address-mutually-exclusive-checkbox",
                            "title": "Were your company based at any of the following addresses?",
                            "answers": [
                                "68 Abingdon Road, Goathill",
                                "7 Evelyn Street, Barry",
                                "251 Argae Lane, Barry",
                                "I prefer not to say",
                            ],
                            "descriptions": None,
                            "guidance": None,
                            "text_length": None,
                            "instruction": None,
                            "answer_description": None,
                            "answer_guidance": None,
                        },
                    },
                    {
                        "question": {
                            "id": "further-details-text-area",
                            "title": "Please provide any further details",
                            "answers": ["Comments"],
                            "descriptions": [
                                "<p>Answer for ESSENTIAL ENTERPRISE LTD.</p>"
                            ],
                            "guidance": None,
                            "text_length": 2000,
                            "instruction": None,
                            "answer_description": None,
                            "answer_guidance": None,
                        },
                    },
                ],
            }
        ]
    }
    assert "groups" in context
    assert_preview_context(context)
    assert len(context["groups"][0]) == 2
    assert "blocks" in context["groups"][0]
    assert context == expected_context
