import pytest


@pytest.fixture
def dynamic_answer_options_schema():
    return {
        "dynamic_options": {
            "values": {
                "map": [
                    {"format-date": ["self", "yyyy-MM-dd"]},
                    {
                        "date-range": [
                            {
                                "date": [
                                    {
                                        "source": "response_metadata",
                                        "identifier": "started_at",
                                    },
                                    {"day_of_week": "MONDAY"},
                                ]
                            },
                            3,
                        ]
                    },
                ]
            },
            "transform": {"format-date": [{"date": ["self"]}, "EEEE d MMMM yyyy"]},
        },
    }


@pytest.fixture
def mock_schema(mocker):
    return mocker.MagicMock()
