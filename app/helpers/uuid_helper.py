from uuid import UUID


def is_valid_uuid(uuid_string, version=4):
    try:
        UUID(uuid_string, version=version)
    except ValueError:
        return False
    return True
