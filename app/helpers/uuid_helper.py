from uuid import UUID


def is_valid_uuid4(uuid_string: str) -> bool:
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True
