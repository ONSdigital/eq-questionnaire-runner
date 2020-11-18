from app.questionnaire.questionnaire_schema import (
    DEFAULT_LANGUAGE_CODE,
    QuestionnaireSchema,
)
from app.utilities.schema import _load_schema_file


def make_schema(data_version, section, group, block, question):
    return {
        "survey_id": "021",
        "data_version": data_version,
        "sections": [
            {
                "id": section,
                "groups": [
                    {
                        "id": group,
                        "blocks": [
                            {"id": block, "type": "Question", "question": question}
                        ],
                    }
                ],
            }
        ],
    }
