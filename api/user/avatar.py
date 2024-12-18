from .base import *

from fastapi import UploadFile


class GetUserAvatarFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.BaseSerializerErrorAppender(
            user_id=fmt.append_serializer_field_error_factory(fmt.transform_id_error_factory('User id')),
        ),
    )

@app.get('/api/user/avatar')
async def get_user_avatar(user_id: Annotated[int, Query(ge=1)]):
    class ErrorCode(IntEnum):
        INVALID_USER_ID = 200

    with db.Session.begin() as session:
        user = mw.get_user_by_id(session, user_id, error_code=ErrorCode.INVALID_USER_ID)
        if not isinstance(user, db.User):
            return JSONResponse(user, status_code=422)
        return Response(user.user_info.get_avatar(db.minio_client))

RequestValidationErrorHandler.register_handler(
    '/api/user/avatar', HttpMethod.GET,
    default_request_validation_error_handler_factory(GetUserAvatarFormatter.format_serializer_errors)
)


class UpdateUserAvatarFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        body=fmt.BaseSerializerErrorAppender(
            avatar=fmt.append_serializer_field_error_factory(fmt.transform_file_error_factory('Avatar')),
        ),
        cookie=fmt.APISerializerErrorAppender(),
    )

    @classmethod
    def get_invalid_content_type_error() -> fmt.ErrorTrace:
        return {
            'avatar': [{ 'type': fmt.FieldErrorCode, 'message': 'Invalid avatar content type' }]
        }

@app.post('/api/user/avatar')
async def update_user_avatar(
    avatar: UploadFile,
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    format: db.models.UserAvatarFormat | None = \
        next(filter(lambda x: x.value[1] == avatar.content_type, db.models.UserAvatarFormat), None)
    if format is None:
        return JSONResponse(UpdateUserAvatarFormatter.get_invalid_content_type_error(), status_code=422)
    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        api_key.user.user_info.update_avatar(
            db.minio_client, db.FileStream(avatar.file, format, avatar.size)
        )
    return JSONResponse({})

RequestValidationErrorHandler.register_handler(
    '/api/user/avatar', HttpMethod.POST,
    default_request_validation_error_handler_factory(UpdateUserAvatarFormatter.format_serializer_errors)
)
