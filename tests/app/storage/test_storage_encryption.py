import pytest

from app.storage.storage_encryption import StorageEncryption
from app.utilities.json import json_loads


@pytest.mark.parametrize(
    "user_id,user_ik,pepper",
    (
        (None, "key", "pepper"),
        ("1", None, "pepper"),
        ("user_id", "user_ik", None),
    ),
)
def test_encrypted_storage_missing_required_args(user_id, user_ik, pepper):
    with pytest.raises(ValueError):
        StorageEncryption(user_id, user_ik, pepper)


@pytest.mark.parametrize(
    "storage1,storage2,storage3",
    (
        (
            ("user1", "user_ik_1", "pepper"),
            ("user1", "user_ik_1", "pepper"),
            ("user2", "user_ik_2", "pepper"),
        ),
        (
            ("user1", "user_ik_1", "pepper"),
            ("user1", "user_ik_1", "pepper"),
            ("user2", "user_ik_1", "pepper"),
        ),
        (
            ("user1", "user_ik_1", "pepper"),
            ("user1", "user_ik_1", "pepper"),
            ("user1", "user_ik_2", "pepper"),
        ),
    ),
)
def test_generate_keys(storage1, storage2, storage3):
    key1 = StorageEncryption(*storage1).key["k"]
    key2 = StorageEncryption(*storage2).key["k"]
    key3 = StorageEncryption(*storage3).key["k"]
    assert key1 == key2
    assert key1 != key3
    assert key2 != key3


def test_encryption_decryption():
    data = {"data1": "Test Data One", "data2": "Test Data Two"}
    encrypter = StorageEncryption("user_id", "user_ik", "pepper")
    encrypted_data = encrypter.encrypt_data(data)
    assert encrypted_data != data
    assert isinstance(encrypted_data, str)

    decrypted_data = encrypter.decrypt_data(encrypted_data)
    decrypted_data = json_loads(decrypted_data)
    assert data == decrypted_data
