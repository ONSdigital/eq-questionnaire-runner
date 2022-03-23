from uuid import UUID

DEFAULT_UUID_VERSION = 4


def is_valid_uuid(uuid_string: str, version: int = DEFAULT_UUID_VERSION) -> bool:
    try:
        UUID(uuid_string, version=version)
    except ValueError:
        return False
    return True
