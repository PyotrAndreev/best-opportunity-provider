from .base import *

from fastapi import UploadFile


class GetUserCVsFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        cookie=fmt.APISerializerErrorAppender(),
    )

@app.get('/api/user/cvs')
async def get_user_cvs(
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        cvs = api_key.user.user_info.get_cvs()
    return JSONResponse(cvs)

RequestValidationErrorHandler.register_handler(
    '/api/user/cvs', HttpMethod.GET,
    default_request_validation_error_handler_factory(GetUserCVsFormatter.format_serializer_errors)
)


class AddCVFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        body=fmt.BaseSerializerErrorAppender(
            cv=fmt.append_serializer_field_error_factory(fmt.transform_file_error_factory('CV')),
        ),
        cookie=fmt.APISerializerErrorAppender(),
    )

    @classmethod
    def get_invalid_content_type_error() -> fmt.ErrorTrace:
        return {
            'cv': [{ 'type': fmt.FieldErrorCode, 'message': 'Invalid CV content type' }]
        }

@app.post('/api/cv')
async def add_cv(
    cv: UploadFile,
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    format: db.models.CVFormat | None = \
        next(filter(lambda x: x.value[1] == cv.content_type, list(db.models.CVFormat)), None)
    if format is None:
        return JSONResponse(AddCVFormatter.get_invalid_content_type_error(), status_code=422)
    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        db.CV.add(
            session, db.minio_client, api_key.user,
            db.File(cv.file, format, cv.size), cv.filename[:50]
        )
    return JSONResponse({})

RequestValidationErrorHandler.register_handler(
    '/api/cv', HttpMethod.POST,
    default_request_validation_error_handler_factory(AddCVFormatter.format_serializer_errors)
)


class CVQueryParameters(BaseModel):
    model_config = {'extra': 'ignore'}

    cv_id: db.serializers.Id

CVQueryParametersAppender = fmt.BaseSerializerErrorAppender(
    cv_id=fmt.append_serializer_field_error_factory(fmt.transform_id_error_factory('CV id')),
)

class RenameCVFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=CVQueryParametersAppender,
        body=fmt.BaseSerializerErrorAppender(
            name=fmt.append_serializer_field_error_factory(
                fmt.transform_str_error_factory('CV name', min_length=1, max_length=50)),
        ),
        cookie=fmt.APISerializerErrorAppender(),
    )

    @classmethod
    def get_insufficient_permissions_error(field_name: str, error_code: int):
        return {field_name: [{'type': error_code, 'message': 'Can\'t rename CV with provided id'}]}

@app.patch('/api/cv/name')
async def rename_cv(
    query: Annotated[CVQueryParameters, Query()],
    body: db.serializers.CV.Rename,
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_CV_ID = 200
        INSUFFICIENT_PERMISSIONS = 201

    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        cv = mw.get_cv_by_id(
            session, query.cv_id, error_code=ErrorCode.INVALID_CV_ID
        )
        if not isinstance(cv, db.CV):
            return JSONResponse(cv, status_code=422)
        if cv.user_info_id != api_key.user_id:
            return JSONResponse(
                RenameCVFormatter.get_insufficient_permissions_error(
                    'api_key', ErrorCode.INSUFFICIENT_PERMISSIONS),
                status_code=422
            )
        cv.rename(body.name)
    return JSONResponse({})

RequestValidationErrorHandler.register_handler(
    '/api/cv/name', HttpMethod.PATCH,
    default_request_validation_error_handler_factory(RenameCVFormatter.format_serializer_errors)
)


class DeleteCVFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=QueryParametersAppender,
        cookie=fmt.APISerializerErrorAppender(),
    )

    @classmethod
    def get_insufficient_permissions_error(field_name: str, error_code: int):
        return {field_name: [{'type': error_code, 'message': 'Can\'t delete CV with provided id'}]}

@app.delete('/api/cv')
async def delete_cv(
    query: Annotated[CVQueryParameters, Query()],
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_CV_ID = 200
        INSUFFICIENT_PERMISSIONS = 201

    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        cv = mw.get_cv_by_id(
            session, query.cv_id, error_code=ErrorCode.INVALID_CV_ID
        )
        if not isinstance(cv, db.CV):
            return JSONResponse(cv, status_code=422)
        if cv.user_info_id != api_key.user_id:
            return JSONResponse(
                DeleteCVFormatter.get_insufficient_permissions_error(
                    'api_key', ErrorCode.INSUFFICIENT_PERMISSIONS
                ),
                status_code=422
            )
        cv.delete(session, db.minio_client)
    return JSONResponse({})

RequestValidationErrorHandler.register_handler(
    '/api/cv', HttpMethod.DELETE,
    default_request_validation_error_handler_factory(DeleteCVFormatter.format_serializer_errors)
)
