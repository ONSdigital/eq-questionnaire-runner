from app.authentication.no_questionnaire_state_exception import (
    NoQuestionnaireStateException,
)


def test_no_questionnaire_state_exception():
    no_token = NoQuestionnaireStateException("test")
    assert "test" == str(no_token)
