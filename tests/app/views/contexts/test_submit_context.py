import pytest

from app.utilities.schema import load_schema_from_name
from app.views.contexts import SubmitQuestionnaireContext
from tests.app.views.contexts import assert_summary_context


@pytest.mark.parametrize(
    "schema_name, expected",
    (
        (
            "test_instructions",
            {
                "title": "Check your answers and submit",
                "guidance": "Please submit this survey to complete it",
                "warning": None,
                "submit_button": "Submit answers",
            },
        ),
        (
            "test_submit_with_custom_submission_text",
            {
                "title": "Submit your questionnaire",
                "guidance": "Thank you for your answers, submit this to complete it",
                "warning": "You cannot view your answers after submission",
                "submit_button": "Submit",
            },
        ),
    ),
)
def test_custom_submission_content(
    schema_name,
    expected,
    data_stores,
):
    schema = load_schema_from_name(schema_name)
    submit_questionnaire_context = SubmitQuestionnaireContext(
        "en",
        schema,
        data_stores,
    )

    context = submit_questionnaire_context()

    assert context["title"] == expected["title"]
    assert context["guidance"] == expected["guidance"]
    assert context["warning"] == expected["warning"]
    assert context["submit_button"] == expected["submit_button"]
    assert "summary" not in context


@pytest.mark.usefixtures("app")
def test_questionnaire_context(data_stores):
    schema = load_schema_from_name("test_submit_with_summary")
    submit_questionnaire_context = SubmitQuestionnaireContext("en", schema, data_stores)

    context = submit_questionnaire_context()
    assert_summary_context(context)
