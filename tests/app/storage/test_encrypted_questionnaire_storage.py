from datetime import datetime, timezone

import pytest

from app.data_models import QuestionnaireStore
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage
from tests.app.conftest import RESPONSE_EXPIRY


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "user_id,user_ik,pepper",
    (
        (None, "key", "pepper"),
        ("1", None, "pepper"),
    ),
)
def test_encrypted_storage_requires_user_id(user_id, user_ik, pepper):
    with pytest.raises(ValueError):
        EncryptedQuestionnaireStorage(user_id, user_ik, pepper)


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "submitted_at", (None, datetime.now(timezone.utc).replace(microsecond=0))
)
def test_store_and_get_submitted_at(submitted_at):
    encrypted = EncryptedQuestionnaireStorage(user_id="1", user_ik="2", pepper="pepper")
    encrypted.save(
        data="test",
        collection_exercise_sid="ce_sid",
        submitted_at=submitted_at,
        expires_at=RESPONSE_EXPIRY,
    )
    # check we can decrypt the data
    assert (
        "test",
        "ce_sid",
        QuestionnaireStore.LATEST_VERSION,
        submitted_at,
    ) == encrypted.get_user_data()


@pytest.mark.usefixtures("app")
def test_store(encrypted_storage):
    data = "test"
    assert encrypted_storage.save(data, "ce_sid") is None
    assert encrypted_storage.get_user_data() is not None


@pytest.mark.usefixtures("app")
def test_get(encrypted_storage):
    data = "test"
    encrypted_storage.save(data, "ce_sid", expires_at=RESPONSE_EXPIRY)
    assert (
        data,
        "ce_sid",
        QuestionnaireStore.LATEST_VERSION,
        None,
    ) == encrypted_storage.get_user_data()


@pytest.mark.usefixtures("app")
def test_delete(encrypted_storage):
    data = "test"
    encrypted_storage.save(data, "ce_sid", expires_at=RESPONSE_EXPIRY)
    assert (
        data,
        "ce_sid",
        QuestionnaireStore.LATEST_VERSION,
        None,
    ) == encrypted_storage.get_user_data()
    encrypted_storage.delete()
    assert (None, None, None, None) == encrypted_storage.get_user_data()
