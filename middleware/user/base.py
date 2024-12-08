from ..base import *


def get_user_by_id(
    session: Session, id: db.serializers.Id, *, 
    error_code: int, field_name: str = 'user_id'
) -> db.User | fmt.FormattedError:
    user: db.User | None = session.get(db.User, id)
    return user if user else {
        field_name: [{'type': error_code, 'message': 'User with provided id doesn\'t exist'}]
    }
