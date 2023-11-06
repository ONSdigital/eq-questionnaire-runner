import pytest
from werkzeug.exceptions import Unauthorized

from app.helpers.schema_helpers import with_schema
from app.questionnaire import QuestionnaireSchema


@pytest.mark.usefixtures("app")
def test_questionnaire_schema_passed_into_function(
    mocker, session_store, fake_questionnaire_store
):
    mocker.patch(
        "app.helpers.schema_helpers.get_metadata",
        return_value=fake_questionnaire_store.stores.metadata,
    )

    mocker.patch(
        "app.helpers.schema_helpers.get_session_store",
        return_value=session_store,
    )

    mock_callable = mocker.Mock()
    func = with_schema(mock_callable)

    func()

    assert isinstance(mock_callable.call_args.args[0], QuestionnaireSchema)


@pytest.mark.usefixtures("app")
def test_no_session_store_raises_unauthorised_exception(mocker):
    mock_callable = mocker.Mock()
    func = with_schema(mock_callable)

    with pytest.raises(Unauthorized):
        assert func()
