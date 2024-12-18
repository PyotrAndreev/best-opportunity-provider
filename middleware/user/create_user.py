from ..base import *


class CreateUserFormatter(fmt.BaseDBFormatter):
    class ErrorCode(IntEnum):
        NON_UNIQUE_EMAIL = 200

    @staticmethod
    def transform_non_unique_email_error(*_) -> fmt.FormattedError:
        return CreateUserFormatter.ErrorCode.NON_UNIQUE_EMAIL, 'User with provided email already exists'

    db_error_appender = fmt.BaseDBErrorAppender({
        db.models.CreateUserErrorCode.NON_UNIQUE_EMAIL:
            fmt.append_db_field_error_factory('email', transformer=transform_non_unique_email_error),
    })

def create_user(
    session: Session, credentials: db.serializers.User.Credentials
) -> db.User | fmt.ErrorTrace:
    """
    :param session: Database session to perform operation on.
                    If user creation fails, `session` don't have to be rolled back.
    :param credentials: Credentials to create user with.

    :returns: Created `User` instance, if creation succeeded,
              `ErrorTrace` with field errors otherwise.
    """

    user = db.User.create(session, credentials)
    if not isinstance(user, db.User):
        return CreateUserFormatter.format_db_errors([user])
    return user
