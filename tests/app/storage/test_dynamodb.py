import pytest

from app.data_models.app_models import QuestionnaireState
from app.storage.errors import ItemAlreadyExistsError


def _assert_item(dynamodb, version):
    item = dynamodb.get(QuestionnaireState, "someuser")
    actual_version = item.version if item else None
    assert actual_version == version


def _put_item(dynamodb, version, overwrite=True):
    model = QuestionnaireState("someuser", "data", "ce_sid", version)
    dynamodb.put(model, overwrite)


@pytest.mark.usefixtures("app")
def test_get_update(dynamodb):
    _assert_item(dynamodb, None)
    _put_item(dynamodb, 1)
    _assert_item(dynamodb, 1)
    _put_item(dynamodb, 2)
    _assert_item(dynamodb, 2)


@pytest.mark.usefixtures("app")
def test_dont_overwrite(dynamodb):
    _put_item(dynamodb, 1)
    with pytest.raises(ItemAlreadyExistsError):
        _put_item(dynamodb, 1, overwrite=False)


@pytest.mark.usefixtures("app")
def test_delete(dynamodb):
    _put_item(dynamodb, 1)
    _assert_item(dynamodb, 1)
    model = QuestionnaireState("someuser", "data", "ce_sid", 1)
    dynamodb.delete(model)
    _assert_item(dynamodb, None)
