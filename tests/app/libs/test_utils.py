from app.helpers.uuid_helper import is_valid_uuid4
from app.libs.utils import convert_tx_id


def test_convert_tx_id():
    tx_id_to_convert = "bc26d5ef-8475-4710-ac82-753a0a150708"

    assert is_valid_uuid4(tx_id_to_convert)
    assert convert_tx_id(tx_id_to_convert) == "BC26 - D5EF - 8475 - 4710"
