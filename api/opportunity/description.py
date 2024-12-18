from .base import *

from fastapi import UploadFile


class GetOpportunityDescriptionQueryParameters(BaseModel):
    model_config = {'extra': 'ignore'}

    opportunity_id: db.serializers.Id

class GetOpportunityDescriptionFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.BaseSerializerErrorAppender(
            opportunity_id=fmt.append_serializer_field_error_factory(
                fmt.transform_id_error_factory("Opportunity id")),
        ),
        cookie=fmt.APISerializerErrorAppender(),
    )

@app.get('/api/opportunity/description')
async def get_opportunity_description(
    query: Annotated[GetOpportunityDescriptionQueryParameters, Query()],
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
):
    class ErrorCode(IntEnum):
        INVALID_OPPORTUNITY_ID = 200

    with db.Session.begin() as session:
        api_key = mw.get_any_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.APIKey.KeysUnion):
            return JSONResponse(api_key, status_code=422)
        opportunity = mw.get_opportunity_by_id(
            session, query.opportunity_id, error_code=ErrorCode.INVALID_OPPORTUNITY_ID
        )
        if not isinstance(opportunity, db.Opportunity):
            return JSONResponse(opportunity, status_code=422)
        return Response(opportunity.get_description(db.minio_client), media_type='text/markdown')

RequestValidationErrorHandler.register_handler(
    '/api/opportunity/description', HttpMethod.GET,
    default_request_validation_error_handler_factory(GetOpportunityDescriptionFormatter.format_serializer_errors)
)


class UpdateOpportunityDescriptionFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=QueryParametersAppender,
        body=fmt.BaseSerializerErrorAppender(
            description=fmt.append_serializer_field_error_factory(fmt.transform_file_error_factory('Description')),
        )
    )

    @classmethod
    def get_invalid_content_type_error(cls) -> fmt.ErrorTrace:
        return {
            'description': [{ 'type': fmt.FieldErrorCode.WRONG_TYPE, 'message': 'Description must be a Markdown file' }]
        }

@app.put('/api/private/opportunity/description')
def update_opportunity_description(
    query: Annotated[QueryParameters, Query()],
    description: UploadFile,
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_OPPORTUNITY_ID = 200

    # Temporary solution, FastAPI doesn't support file content type validation
    if description.content_type != 'text/markdown':
        return JSONResponse(UpdateOpportunityDescriptionFormatter.get_invalid_content_type_error(),
                            status_code=422)
    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        opportunity = mw.get_opportunity_by_id(
            session, query.opportunity_id, error_code=ErrorCode.INVALID_OPPORTUNITY_ID
        )
        if not isinstance(opportunity, db.Opportunity):
            return JSONResponse(opportunity, status_code=422)
        opportunity.update_description(db.minio_client, db.FileStream(description.file, None, description.size))
    return JSONResponse({})

RequestValidationErrorHandler.register_handler(
    '/api/private/opportunity/description', HttpMethod.PUT,
    default_request_validation_error_handler_factory(UpdateOpportunityDescriptionFormatter.format_serializer_errors)
)
