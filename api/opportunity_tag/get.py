from ..base import *


class GetAllOpportunityTagsPrivateFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.APISerializerErrorAppender(),
    )

@app.get('/api/private/opportunity-tag/all')
def get_all_opportunity_tags_private(
    query: Annotated[db.serializers.APIKeyModel, Query()],
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        return JSONResponse(db.OpportunityTag.get_all(session))

RequestValidationErrorHandler.register_handler(
    '/api/private/opportunity-tag/all', HttpMethod.GET,
    default_request_validation_error_handler_factory(
        GetAllOpportunityTagsPrivateFormatter.format_serializer_errors)
)


class GetAllOpportunityTagsPublicFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        cookie=fmt.APISerializerErrorAppender(),
    )

@app.get('/api/opportunity-tag/all')
async def get_all_opportunity_tags_public(
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        return JSONResponse(db.OpportunityTag.get_all(session))

RequestValidationErrorHandler.register_handler(
    '/api/opportunity-tag/all', HttpMethod.GET,
    default_request_validation_error_handler_factory(GetAllOpportunityTagsPublicFormatter.format_serializer_errors)
)
