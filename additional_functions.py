from uuid import UUID


def is_valid_uuid(uuid: str) -> bool:
    try:
        uuid = UUID(uuid)
    except ValueError:
        return False
    return True
