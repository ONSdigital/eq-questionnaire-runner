import pytest

from app.data_models.app_models import QuestionnaireState
from app.storage.errors import ItemAlreadyExistsError


def _assert_item(ddb, version):
    item = ddb.get(QuestionnaireState, "someuser")
    actual_version = item.version if item else None
    assert actual_version == version


def _put_item(ddb, version, overwrite=True):
    model = QuestionnaireState("someuser", "data", "ce_sid", version)
    ddb.put(model, overwrite)


@pytest.mark.usefixtures("app")
def test_get_update(ddb):
    _assert_item(ddb, None)
    _put_item(ddb, 1)
    _assert_item(ddb, 1)
    _put_item(ddb, 2)
    _assert_item(ddb, 2)


@pytest.mark.usefixtures("app")
def test_dont_overwrite(ddb):
    _put_item(ddb, 1)
    with pytest.raises(ItemAlreadyExistsError):
        _put_item(ddb, 1, overwrite=False)


@pytest.mark.usefixtures("app")
def test_delete(ddb):
    _put_item(ddb, 1)
    _assert_item(ddb, 1)
    model = QuestionnaireState("someuser", "data", "ce_sid", 1)
    ddb.delete(model)
    _assert_item(ddb, None)
