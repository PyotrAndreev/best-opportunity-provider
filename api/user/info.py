from .base import *


UpdateUserInfoAppender = fmt.BaseSerializerErrorAppender(
    name=fmt.append_serializer_field_error_factory(
        fmt.transform_str_error_factory('Name', min_length=1, max_length=50)
    ),
    surname=fmt.append_serializer_field_error_factory(
        fmt.transform_str_error_factory('Surname', min_length=1, max_length=50)
    ),
    birthday=fmt.append_serializer_nested_model_error_factory(
        transformer=fmt.DateFormatter.transform_root_error,
        # TODO: make consistent with other appenders
        model_error_appender=fmt.DateFormatter.append_serializer_error,
    ),
    city_id=fmt.append_serializer_field_error_factory(fmt.transform_id_error_factory('City id')),
)

class UpdateUserInfoPrivateFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=QueryParametersAppender,
        body=UpdateUserInfoAppender,
    )

@app.patch('/api/private/user/info')
def update_user_info_private(
    query: Annotated[QueryParameters, Query()],
    body: db.serializers.UserInfo.Update,
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_USER_ID = 200

    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        user = mw.get_user_by_id(session, query.user_id, error_code=ErrorCode.INVALID_USER_ID)
        if not isinstance(user, db.User):
            return JSONResponse(user, status_code=422)
        mw.update_user_info(user, body)
    return JSONResponse({})

RequestValidationErrorHandler.register_handler(
    '/api/user/info', HttpMethod.PATCH,
    default_request_validation_error_handler_factory(UpdateUserInfoPrivateFormatter.format_serializer_errors)
)


class UpdateUserInfoPublicFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        body=UpdateUserInfoAppender,
        cookie=fmt.APISerializerErrorAppender(),
    )

@app.patch('/api/user/info')
async def update_user_info_public(
    body: db.serializers.UserInfo.Update,
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        mw.update_user_info(api_key.user.user_info, body)
    return JSONResponse({})
