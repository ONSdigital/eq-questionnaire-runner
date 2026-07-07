def make_schema(data_version, section, group, block, question):
    return {
        "survey_id": "999",
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
