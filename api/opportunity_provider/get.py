from ..base import *


class GetAllOpportunityProvidersPrivate(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.APISerializerErrorAppender(),
    )

@app.get('/api/private/opportunity-provider/all')
def get_all_opportunity_providers_private(
    query: Annotated[db.serializers.APIKeyModel, Query()],
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        return JSONResponse(db.OpportunityProvider.get_all(session))

RequestValidationErrorHandler.register_handler(
    '/api/private/opportunity-provider/all', HttpMethod.GET,
    default_request_validation_error_handler_factory(
        GetAllOpportunityProvidersPrivate.format_serializer_errors)
)


class GetAllOpportunityProvidersPublicFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        cookie=fmt.APISerializerErrorAppender(),
    )

@app.get('/api/opportunity-provider/all')
async def get_all_opportunity_providers_public(
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        return JSONResponse(db.OpportunityProvider.get_all(session))

RequestValidationErrorHandler.register_handler(
    '/api/opportunity-provider/all', HttpMethod.GET,
    default_request_validation_error_handler_factory(GetAllOpportunityProvidersPublicFormatter.format_serializer_errors)
)
