from .base import *


class AddOpportunityTagsFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=QueryParametersAppender,
        body=fmt.BaseSerializerErrorAppender(
            tag_ids=fmt.append_serializer_list_error_factory(
                transformer=fmt.transform_list_error_factory('Tag ids', min_length=1),
                element_error_appender=fmt.append_serializer_field_error_factory(
                    fmt.transform_id_error_factory('Tag id')
                )
            ),
        ),
    )

@app.post('/api/private/opportunity/tags')
def add_opportunity_tags(
    query: Annotated[QueryParameters, Query()],
    body: mw.TagsList,
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_OPPORTUNITY_ID = 200
        INVALID_TAG_ID = 201

    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        opportunity = mw.get_opportunity_by_id(
            session, query.opportunity_id, error_code=ErrorCode.INVALID_OPPORTUNITY_ID
        )
        if not isinstance(opportunity, db.Opportunity):
            return JSONResponse(opportunity, status_code=422)
        error = mw.add_opportunity_tags(
            session, opportunity, body, error_code=ErrorCode.INVALID_TAG_ID
        )
        if error is not None:
            return JSONResponse(error, status_code=422)
    return JSONResponse({})

RequestValidationErrorHandler.register_handler(
    '/api/private/opportunity/tags', HttpMethod.POST,
    default_request_validation_error_handler_factory(AddOpportunityTagsFormatter.format_serializer_errors)
)
