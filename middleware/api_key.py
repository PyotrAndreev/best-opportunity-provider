from .base import *


def get_invalid_api_key_error(*, field_name: str = 'api_key') -> fmt.ErrorTrace:
    error = fmt.APISerializerErrorAppender.transform_invalid_api_key_error()
    return { field_name: [{ 'type': error[0], 'message': error[1] }] }


def get_developer_api_key_or_error(
    session: Session, key: db.serializers.APIKey,
) -> db.DeveloperAPIKey | fmt.ErrorTrace:
    if not (api_key := db.APIKey.get(session, key)) or not isinstance(api_key, db.DeveloperAPIKey):
        return get_invalid_api_key_error()
    return api_key


def get_personal_api_key(
    session: Session, key: db.serializers.APIKey,
) -> db.PersonalAPIKey | None:
    if not (api_key := db.APIKey.get(session, key)) or not isinstance(api_key, db.PersonalAPIKey):
        return None
    return api_key

def get_personal_api_key_or_error(
    session: Session, key: db.serializers.APIKey,
) -> db.PersonalAPIKey | fmt.ErrorTrace:
    api_key = get_personal_api_key(session, key)
    if api_key is None:
        return get_invalid_api_key_error()
    return api_key


def get_any_api_key(
    session: Session, key: db.serializers.APIKey,
) -> db.APIKey.KeysUnion | None:
    return db.APIKey.get(session, key)

def get_any_api_key_or_error(
    session: Session, key: db.serializers.APIKey,
) -> db.APIKey.KeysUnion | fmt.ErrorTrace:
    api_key = get_any_api_key(session, key)
    if api_key is None:
        return get_invalid_api_key_error()
    return api_key
