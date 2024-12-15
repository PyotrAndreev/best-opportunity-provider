from copy import copy
from ipaddress import IPv4Address

from .base import *


class CredentialsFormatter(fmt.BaseSerializerFormatter):
    @staticmethod
    def transform_email_error(error: fmt.PydanticError, _root: int) -> fmt.FormattedError | None:
        match error['type']:
            case 'missing':
                return fmt.FieldErrorCode.MISSING, 'Missing required field'
            case 'string_type':
                return fmt.FieldErrorCode.WRONG_TYPE, 'Email must be a string'
            case 'pattern_error':
                return fmt.FieldErrorCode.INVALID_PATTERN, 'Not a valid email address'

    @staticmethod
    def transform_password_error(error: fmt.PydanticError, _root: int) -> fmt.FormattedError | None:
        match error['type']:
            case 'missing':
                return fmt.FieldErrorCode.MISSING, 'Missing required field'
            case 'string_type':
                return fmt.FieldErrorCode.WRONG_TYPE, 'Password must be a string'
            case 'string_too_short':
                return fmt.FieldErrorCode.LENGTH_NOT_IN_RANGE, 'Password must contain at least 8 characters'
            case 'pattern_error':
                return fmt.FieldErrorCode.INVALID_PATTERN, 'Password must contain at least one lowercase letter, ' \
                                                           'one uppercase letter, one digit and one special character'

    serializer_error_appender = fmt.BaseSerializerErrorAppender(
        email=fmt.append_serializer_field_error_factory(transform_email_error),
        password=fmt.append_serializer_field_error_factory(transform_password_error),
    )


@app.post('/api/private/user')
def create_user(credentials: db.serializers.User.Credentials) -> JSONResponse:
    with db.Session.begin() as session:
        user = mw.create_user(session, credentials)
        if not isinstance(user, db.User):
            session.rollback()
            return JSONResponse(user, status_code=422)
        session.flush([user])
        return JSONResponse({ 'user_id': user.id })

RequestValidationErrorHandler.register_handler(
    '/api/private/user', HttpMethod.POST,
    default_request_validation_error_handler_factory(CredentialsFormatter.format_serializer_errors)
)


class Login(db.serializers.User.Credentials):
    remember_me: bool | None = None

class LoginFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = copy(CredentialsFormatter.serializer_error_appender).update(
        remember_me=fmt.append_serializer_field_error_factory(fmt.transform_bool_error_factory('Remember me'))
    )

@app.post('/api/login')
async def login(request: Request, fields: Login) -> JSONResponse:
    # 'request.client' may be None by specification, but this only occurs when using FastAPI TestClient,
    # which is not currently used. If this changes in the future, do not forget to handle this case
    assert request.client is not None

    with db.Session.begin() as session:
        api_key = mw.authorize_user(session, fields,
                                    ip=IPv4Address(request.client.host),
                                    remember_me=fields.remember_me)
        if api_key is None:
            return JSONResponse({}, status_code=401)
        response = JSONResponse({})
        response.set_cookie('api_key', str(api_key), expires=api_key.expiry_date)
        return response

RequestValidationErrorHandler.register_handler(
    '/api/login', HttpMethod.POST,
    default_request_validation_error_handler_factory(LoginFormatter.format_serializer_errors)
)


@app.post('/api/logout')
def logout(api_key: Annotated[str | None, Cookie()] = None) -> JSONResponse:
    response = JSONResponse({})
    response.delete_cookie('api_key')
    if api_key is None or not db.serializers.assert_api_key(api_key):
        return response
    with db.Session.begin() as session:
        personal_api_key = mw.get_personal_api_key(session, api_key)
        if personal_api_key is None:
            return response
        personal_api_key.expire(session)
    return response
