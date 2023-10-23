import pytest
from flask_babel import lazy_gettext

from app.data_models.data_stores import DataStores
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.preview_context import (
    PreviewContext,
    PreviewNotEnabledException,
)
from tests.app.views.contexts import assert_preview_context


def test_build_preview_rendering_context(
    test_introduction_preview_linear_schema,
    questionnaire_store,
):
    preview_context = PreviewContext(
        "en",
        test_introduction_preview_linear_schema,
        data_stores=DataStores(
            supplementary_data_store=questionnaire_store.data_stores.supplementary_data_store,
            metadata=questionnaire_store.data_stores.metadata,
            response_metadata=questionnaire_store.data_stores.response_metadata,
        ),
    )

    preview_context = preview_context()

    assert_preview_context(preview_context)


def test_build_preview_context(
    test_introduction_preview_linear_schema,
    questionnaire_store,
):
    preview_context = PreviewContext(
        "en",
        test_introduction_preview_linear_schema,
        data_stores=DataStores(
            supplementary_data_store=questionnaire_store.data_stores.supplementary_data_store,
            metadata=questionnaire_store.data_stores.metadata,
            response_metadata=questionnaire_store.data_stores.response_metadata,
        ),
    )
    context = preview_context()

    expected_context = {
        "sections": [
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
                                                "description": "For example select `yes` if you can report for this period"
                                            }
                                        ],
                                        "hide_guidance": "Additional guidance",
                                        "show_guidance": "Additional guidance",
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
                            "answers": [
                                {"label": "Period from"},
                                {"label": "Period to"},
                            ],
                            "descriptions": [
                                "<p>If figures are not available for the calendar year 2021, your return should "
                                "relate to a 12 month business year that ends between 6 April 2021 and 5 April 2022.</p>"
                            ],
                            "guidance": {
                                "contents": [
                                    {
                                        "description": "<p><strong>Only traded for a part of the year?</strong></p>"
                                    },
                                    {
                                        "description": "<p>Please provide figures for the period in which you were trading.</p>"
                                    },
                                    {
                                        "description": "<p><strong>Only commenced trading during 2021?</strong></p>"
                                    },
                                    {
                                        "description": "<p>Your return should cover the period from the commencement of "
                                        "your business until 31 December 2021 or, alternatively, any date up to 5 April 2022.</p>"
                                    },
                                    {
                                        "description": "<p><strong>Ceased trading during 2021?</strong></p>"
                                    },
                                    {
                                        "description": "<p>Your return should cover the period 1 January 2021 to the date "
                                        "you ceased to trade or, alternatively, from the beginning of your last business year up to the cessation date.</p>"
                                    },
                                ]
                            },
                            "id": "reporting-date",
                            "title": "What dates will you be reporting for?",
                            "type": "DateRange",
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
                            "title": "Are you sure you are able to report for the calendar month {calendar_start_date} to {calendar_end_date}?",
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
                "id": "introduction-section",
            }
        ]
    }
    assert "sections" in context
    assert_preview_context(context)
    assert len(context["sections"][0]) == 3
    assert "blocks" in context["sections"][0]
    assert context == expected_context


def test_preview_questions_disabled_raises_exception(
    data_stores,
):
    schema = QuestionnaireSchema({"preview_questions": False})
    with pytest.raises(PreviewNotEnabledException):
        PreviewContext(
            "en",
            schema,
            data_stores,
        )
