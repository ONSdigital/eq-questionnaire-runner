import os
from functools import lru_cache
from glob import glob
from pathlib import Path
from typing import Mapping, Optional

import requests
from structlog import get_logger
from werkzeug.exceptions import NotFound

from app.questionnaire.questionnaire_schema import (
    DEFAULT_LANGUAGE_CODE,
    QuestionnaireSchema,
)
from app.utilities.json import json_load, json_loads

logger = get_logger()

SCHEMA_DIR = "schemas"
LANGUAGE_CODES = ("en", "cy")

LANGUAGES_MAP = {"test_language": [["en", "cy"]]}


@lru_cache(maxsize=None)
def get_schema_list(language_code: str = DEFAULT_LANGUAGE_CODE) -> dict[str, list]:
    return {
        survey_type: list(schemas_by_language[language_code])
        for survey_type, schemas_by_language in get_schema_path_map(
            include_test_schemas=True
        ).items()
        for lang in schemas_by_language
        if lang == language_code
    }


@lru_cache(maxsize=None)
def get_schema_path(language_code, schema_name):
    for schemas_by_language in get_schema_path_map(include_test_schemas=True).values():
        schema_path = schemas_by_language.get(language_code, {}).get(schema_name)
        if schema_path:
            return schema_path


@lru_cache(maxsize=None)
def get_schema_path_map(include_test_schemas: Optional[bool] = False) -> Mapping:
    schemas = {}
    for survey_type in os.listdir(SCHEMA_DIR):
        if not include_test_schemas and survey_type == "test":
            continue

        schemas[survey_type] = {
            language_code: {
                Path(schema_file).with_suffix("").name: schema_file
                for schema_file in glob(
                    f"{SCHEMA_DIR}/{survey_type}/{language_code}/*.json"
                )
            }
            for language_code in LANGUAGE_CODES
        }

    return schemas


def _schema_exists(language_code, schema_name):
    schema_path_map = get_schema_path_map(include_test_schemas=True)
    return any(
        True
        for survey_type, schemas_by_lang in schema_path_map.items()
        if language_code in schemas_by_lang
        and schema_name in schemas_by_lang[language_code]
    )


def get_allowed_languages(schema_name, launch_language):
    for language_combination in LANGUAGES_MAP.get(schema_name, []):
        if launch_language in language_combination:
            return language_combination
    return [DEFAULT_LANGUAGE_CODE]


def load_schema_from_metadata(metadata):
    if metadata.get("survey_url"):
        return load_schema_from_url(
            metadata["survey_url"], metadata.get("language_code")
        )

    return load_schema_from_name(
        metadata.get("schema_name"), language_code=metadata.get("language_code")
    )


def load_schema_from_session_data(session_data):
    return load_schema_from_metadata(vars(session_data))


def load_schema_from_name(schema_name, language_code=DEFAULT_LANGUAGE_CODE):
    cache_info = _load_schema_from_name.cache_info()
    logger.error(f"hey rhys check out this log info: cache_info.miss: {cache_info.misses}, cache_info.hits: {cache_info.hits} cache_info.currsize: {cache_info.currsize}")
    return _load_schema_from_name(schema_name, language_code)


@lru_cache(maxsize=None)
def _load_schema_from_name(schema_name, language_code):
    schema_json = {
        "language": "en",
        "mime_type": "application/json/ons/eq",
        "schema_version": "0.0.1",
        "data_version": "0.0.1",
        "survey_id": "017",
        "form_type": "0070",
        "legal_basis": "Notice is given under section 1 of the Statistics of Trade Act 1947.",
        "title": "Quarterly Stocks Survey",
        "questionnaire_flow": {
            "type": "Linear",
            "options": {
                "summary": {
                    "collapsible": False
                }
            }
        },
        "post_submission": {
            "feedback": True,
            "view_response": True
        },
        "sections": [
            {
                "id": "sectionquestionnaire-introduction",
                "title": "Introduction",
                "groups": [
                    {
                        "id": "groupquestionnaire-introduction",
                        "title": "Introduction",
                        "blocks": [
                            {
                                "id": "introduction-block",
                                "type": "Introduction",
                                "primary_content": [
                                    {
                                        "id": "primary",
                                        "title": {
                                            "text": "You are completing this for {trad_as} ({ru_name})",
                                            "placeholders": [
                                                {
                                                    "placeholder": "trad_as",
                                                    "transforms": [
                                                        {
                                                            "transform": "first_non_empty_item",
                                                            "arguments": {
                                                                "items": [
                                                                    {
                                                                        "source": "metadata",
                                                                        "identifier": "trad_as"
                                                                    },
                                                                    {
                                                                        "source": "metadata",
                                                                        "identifier": "ru_name"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                },
                                                {
                                                    "placeholder": "ru_name",
                                                    "value": {
                                                        "source": "metadata",
                                                        "identifier": "ru_name"
                                                    }
                                                }
                                            ]
                                        },
                                        "contents": [
                                            {
                                                "list": [
                                                    "This survey covers UK businesses. The business is the individual company, partnership or sole proprietorship to which the questionnaire has been sent, unless specified otherwise.",
                                                    "Include all stock owned by your business, whether in the UK or abroad.",
                                                    "We will treat your data securely and confidentially."
                                                ]
                                            }
                                        ]
                                    }
                                ],
                                "preview_content": {
                                    "id": "preview",
                                    "title": "Information you need",
                                    "contents": [
                                        {
                                            "description": "You can select the dates of the period you are reporting for, if the given dates are not appropriate."
                                        },
                                        {
                                            "description": "Include:"
                                        },
                                        {
                                            "list": [
                                                "all stock owned by your business, whether in the UK or abroad",
                                                "duty for dutiable goods held out of bond",
                                                "the value of any goods let out on hire, only if they were charged to current account when acquired and do not rank as capital items for taxation purposes",
                                                "work in progress"
                                            ]
                                        },
                                        {
                                            "description": "Exclude:"
                                        },
                                        {
                                            "list": ["VAT", "stocks you hold that do not belong to you", "duty on stocks held in bond"]
                                        }
                                    ]
                                },
                                "secondary_content": [
                                    {
                                        "id": "secondary-content",
                                        "contents": [
                                            {
                                                "title": "How we use your data"
                                            },
                                            {
                                                "list": [
                                                    "The information supplied is used to estimate changes in stock levels which are used in the compilation of Gross Domestic Product (GDP), the total UK economic activity.",
                                                    "GDP is used to measure the UK&apos;s financial health and prosperity over time and in comparison to other countries.",
                                                    "The results are used by the Bank of England and HM Treasury to monitor interest rates, inflation and in formulating financial policies (e.g. income, expenditure and taxation) for the UK."
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "id": "section91",
                "title": "Quarterly Stocks Survey",
                "groups": [
                    {
                        "id": "group91",
                        "blocks": [
                            {
                                "id": "block379",
                                "type": "Question",
                                "question": {
                                    "id": "question379",
                                    "title": {
                                        "text": "Are you able to report for the period {ref_p_start_date} to {ref_p_end_date}?",
                                        "placeholders": [
                                            {
                                                "placeholder": "ref_p_start_date",
                                                "transforms": [
                                                    {
                                                        "transform": "format_date",
                                                        "arguments": {
                                                            "date_to_format": {
                                                                "source": "metadata",
                                                                "identifier": "ref_p_start_date"
                                                            },
                                                            "date_format": "d MMMM yyyy"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "placeholder": "ref_p_end_date",
                                                "transforms": [
                                                    {
                                                        "transform": "format_date",
                                                        "arguments": {
                                                            "date_to_format": {
                                                                "source": "metadata",
                                                                "identifier": "ref_p_end_date"
                                                            },
                                                            "date_format": "d MMMM yyyy"
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    "type": "General",
                                    "answers": [
                                        {
                                            "id": "answer434",
                                            "mandatory": True,
                                            "type": "Radio",
                                            "options": [
                                                {
                                                    "label": "Yes",
                                                    "value": "Yes"
                                                },
                                                {
                                                    "label": "No",
                                                    "value": "No"
                                                }
                                            ]
                                        }
                                    ]
                                },
                                "routing_rules": [
                                    {
                                        "goto": {
                                            "block": "block381",
                                            "when": [
                                                {
                                                    "id": "answer434",
                                                    "condition": "equals any",
                                                    "values": ["Yes"]
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        "goto": {
                                            "block": "block380"
                                        }
                                    }
                                ]
                            },
                            {
                                "id": "block380",
                                "type": "Question",
                                "question": {
                                    "id": "question380",
                                    "title": "For which period are you able to report?",
                                    "type": "DateRange",
                                    "answers": [
                                        {
                                            "id": "answerfrom",
                                            "type": "Date",
                                            "mandatory": True,
                                            "label": "Period from",
                                            "q_code": "11",
                                            "minimum": {
                                                "value": {
                                                    "source": "metadata",
                                                    "identifier": "ref_p_start_date"
                                                },
                                                "offset_by": {
                                                    "days": -31
                                                }
                                            }
                                        },
                                        {
                                            "id": "answerto",
                                            "type": "Date",
                                            "mandatory": True,
                                            "label": "Period to",
                                            "q_code": "12",
                                            "maximum": {
                                                "value": {
                                                    "source": "metadata",
                                                    "identifier": "ref_p_end_date"
                                                },
                                                "offset_by": {
                                                    "days": 31
                                                }
                                            }
                                        }
                                    ],
                                    "period_limits": {
                                        "minimum": {
                                            "days": 76
                                        },
                                        "maximum": {
                                            "days": 106
                                        }
                                    }
                                }
                            },
                            {
                                "id": "block381",
                                "type": "Question",
                                "question": {
                                    "id": "question381",
                                    "title": "What was the <em>total value</em> of stocks held (net of progress payments on long-term contracts)?",
                                    "guidance": {
                                        "contents": [
                                            {
                                                "description": "Include:"
                                            },
                                            {
                                                "list": [
                                                    "all stock owned by your business, whether in the UK or abroad",
                                                    "duty for dutiable goods held out of bond",
                                                    "the value of any goods let out on hire, only if they were charged to current account when acquired and do not rank as capital items for taxation purposes",
                                                    "work in progress"
                                                ]
                                            },
                                            {
                                                "description": "Exclude:"
                                            },
                                            {
                                                "list": ["VAT", "stocks you hold that do not belong to you", "duty on stocks held in bond"]
                                            }
                                        ]
                                    },
                                    "definitions": [
                                        {
                                            "title": "What is work in progress?",
                                            "contents": [
                                                {
                                                    "description": "This refers to goods and services that have been partially completed (e.g. a solicitor working on a legal case over a period of time and being paid at the end of the contract for the services provided i.e. unbilled work)."
                                                }
                                            ]
                                        }
                                    ],
                                    "type": "General",
                                    "answers": [
                                        {
                                            "id": "answer436",
                                            "mandatory": True,
                                            "type": "Currency",
                                            "label": "Total value of stocks held at start of period",
                                            "description": "Enter the full value (e.g. 56,234.33) or a value to the nearest £thousand (e.g. 56,000). Do not enter ‘56’ for £56,000.",
                                            "q_code": "598",
                                            "decimal_places": 2,
                                            "currency": "GBP"
                                        },
                                        {
                                            "id": "answer437",
                                            "mandatory": True,
                                            "type": "Currency",
                                            "label": "Total value of stocks held at end of period",
                                            "description": "Enter the full value (e.g. 56,234.33) or a value to the nearest £thousand (e.g. 56,000). Do not enter ‘56’ for £56,000.",
                                            "q_code": "599",
                                            "decimal_places": 2,
                                            "currency": "GBP"
                                        }
                                    ]
                                }
                            },
                            {
                                "id": "block4616",
                                "type": "Question",
                                "question": {
                                    "id": "question4616",
                                    "title": "Are the end of period figures you have provided estimated?",
                                    "type": "General",
                                    "answers": [
                                        {
                                            "id": "answer5873",
                                            "mandatory": True,
                                            "type": "Radio",
                                            "q_code": "15",
                                            "options": [
                                                {
                                                    "label": "Yes",
                                                    "value": "Yes"
                                                },
                                                {
                                                    "label": "No",
                                                    "value": "No"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            },
                            {
                                "id": "block4952",
                                "type": "Question",
                                "question": {
                                    "id": "question4952",
                                    "title": {
                                        "text": "Did any significant changes occur to the total value of stocks for {trad_as}?",
                                        "placeholders": [
                                            {
                                                "placeholder": "trad_as",
                                                "transforms": [
                                                    {
                                                        "transform": "first_non_empty_item",
                                                        "arguments": {
                                                            "items": [
                                                                {
                                                                    "source": "metadata",
                                                                    "identifier": "trad_as"
                                                                },
                                                                {
                                                                    "source": "metadata",
                                                                    "identifier": "ru_name"
                                                                }
                                                            ]
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    "description": [
                                        {
                                            "text": "<p>Please note: what constitutes a &#x2018;significant change&#x2019; is dependent on your own interpretation in relation to {trad_as}&#x2019;s figures from the previous reporting period and the same reporting period last year.</p><p>This information will help us to validate your data and should reduce the need to query any figures with you.</p>",
                                            "placeholders": [
                                                {
                                                    "placeholder": "trad_as",
                                                    "transforms": [
                                                        {
                                                            "transform": "first_non_empty_item",
                                                            "arguments": {
                                                                "items": [
                                                                    {
                                                                        "source": "metadata",
                                                                        "identifier": "trad_as"
                                                                    },
                                                                    {
                                                                        "source": "metadata",
                                                                        "identifier": "ru_name"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ],
                                    "type": "General",
                                    "answers": [
                                        {
                                            "id": "answer6287",
                                            "mandatory": True,
                                            "type": "Radio",
                                            "q_code": "146a",
                                            "options": [
                                                {
                                                    "label": "Yes",
                                                    "value": "Yes"
                                                },
                                                {
                                                    "label": "No",
                                                    "value": "No"
                                                }
                                            ]
                                        }
                                    ]
                                },
                                "routing_rules": [
                                    {
                                        "goto": {
                                            "block": "block4953",
                                            "when": [
                                                {
                                                    "id": "answer6287",
                                                    "condition": "equals any",
                                                    "values": ["Yes"]
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        "goto": {
                                            "block": "block383"
                                        }
                                    }
                                ]
                            },
                            {
                                "id": "block4953",
                                "type": "Question",
                                "question": {
                                    "id": "question4953",
                                    "title": {
                                        "text": "Please indicate the reasons for any changes in the total value of stocks for {trad_as}",
                                        "placeholders": [
                                            {
                                                "placeholder": "trad_as",
                                                "transforms": [
                                                    {
                                                        "transform": "first_non_empty_item",
                                                        "arguments": {
                                                            "items": [
                                                                {
                                                                    "source": "metadata",
                                                                    "identifier": "trad_as"
                                                                },
                                                                {
                                                                    "source": "metadata",
                                                                    "identifier": "ru_name"
                                                                }
                                                            ]
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    "type": "General",
                                    "answers": [
                                        {
                                            "id": "answer6288",
                                            "mandatory": True,
                                            "type": "Checkbox",
                                            "options": [
                                                {
                                                    "label": "Change of business structure, merger or takeover",
                                                    "value": "Change of business structure, merger or takeover",
                                                    "q_code": "146e"
                                                },
                                                {
                                                    "label": "End of accounting period or financial year",
                                                    "value": "End of accounting period or financial year",
                                                    "q_code": "146c"
                                                },
                                                {
                                                    "label": "Introduction or removal of new legislation or incentive",
                                                    "value": "Introduction or removal of new legislation or incentive",
                                                    "q_code": "146g"
                                                },
                                                {
                                                    "label": "Normal movement for the time of year",
                                                    "value": "Normal movement for the time of year",
                                                    "q_code": "146d"
                                                },
                                                {
                                                    "label": "One-off increase in stocks",
                                                    "value": "One-off increase in stocks",
                                                    "q_code": "146f"
                                                },
                                                {
                                                    "label": "Start or end of long term project",
                                                    "value": "Start or end of long term project",
                                                    "q_code": "146b"
                                                },
                                                {
                                                    "label": "Other (for example, end of the EU transition period, leaving the EU or other global economic conditions.",
                                                    "value": "Other (for example, end of the EU transition period, leaving the EU or other global economic conditions.",
                                                    "q_code": "146h"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            },
                            {
                                "id": "block383",
                                "type": "Question",
                                "question": {
                                    "id": "question383",
                                    "title": "Explain any differences between this quarter&apos;s opening value and the previously returned closing value",
                                    "description": ["<p>  Include any unusual fluctuations in figures  </p>"],
                                    "type": "General",
                                    "answers": [
                                        {
                                            "id": "answer439",
                                            "mandatory": False,
                                            "type": "TextArea",
                                            "label": "Comments",
                                            "q_code": "146",
                                            "max_length": 2000
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "theme": "default",
        "navigation": {
            "visible": False
        },
        "metadata": [
            {
                "name": "user_id",
                "type": "string"
            },
            {
                "name": "period_id",
                "type": "string"
            },
            {
                "name": "ru_name",
                "type": "string"
            },
            {
                "name": "ref_p_start_date",
                "type": "date"
            },
            {
                "name": "ref_p_end_date",
                "type": "date"
            },
            {
                "name": "trad_as",
                "type": "string",
                "optional": True
            }
        ]
    }

    return QuestionnaireSchema(schema_json, language_code)


def get_schema_name_from_params(eq_id, form_type):
    return f"{eq_id}_{form_type}"


def _load_schema_file(schema_name, language_code):
    """
    Load a schema, optionally for a specified language.
    :param schema_name: The name of the schema e.g. census_household
    :param language_code: ISO 2-character code for language e.g. 'en', 'cy'
    """
    if language_code != DEFAULT_LANGUAGE_CODE and not _schema_exists(
        language_code, schema_name
    ):
        language_code = DEFAULT_LANGUAGE_CODE
        logger.info(
            "couldn't find requested language schema, falling back to 'en'",
            schema_file=schema_name,
            language_code=language_code,
        )

    if not _schema_exists(language_code, schema_name):
        logger.error(
            "no schema file exists",
            schema_name=schema_name,
            language_code=language_code,
        )
        raise FileNotFoundError

    schema_path = get_schema_path(language_code, schema_name)

    logger.info(
        "loading schema",
        schema_name=schema_name,
        language_code=language_code,
        schema_path=schema_path,
    )

    with open(schema_path, encoding="utf8") as json_file:
        return json_load(json_file)


def load_schema_from_url(survey_url, language_code):
    language_code = language_code or DEFAULT_LANGUAGE_CODE
    logger.info(
        "loading schema from URL", survey_url=survey_url, language_code=language_code
    )

    constructed_survey_url = f"{survey_url}?language={language_code}"

    req = requests.get(constructed_survey_url)
    schema_response = req.content.decode()

    if req.status_code == 404:
        logger.error("no schema exists", survey_url=constructed_survey_url)
        raise NotFound

    return QuestionnaireSchema(json_loads(schema_response), language_code)


def cache_questionnaire_schemas():
    for schemas_by_language in get_schema_path_map().values():
        logger.error(f"Caching schemas for {get_schema_path_map().values()}")
        for language_code, schemas in schemas_by_language.items():
            for schema in schemas:
                load_schema_from_name(schema, language_code)
