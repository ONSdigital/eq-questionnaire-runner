from uuid import UUID


def is_valid_uuid(uuid_string: str, version: int = 4) -> bool:
    try:
        UUID(uuid_string, version=version)
    except ValueError:
        return False
    return True
