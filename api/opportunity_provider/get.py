from ..base import *


class GetAllProvidersFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        cookie=fmt.APISerializerErrorAppender(),
    )

@app.get('/api/opportunity-provider/all')
async def get_all_providers(
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        return JSONResponse(db.OpportunityProvider.get_all(session))

RequestValidationErrorHandler.register_handler(
    '/api/opportunity-provider/all', HttpMethod.GET,
    default_request_validation_error_handler_factory(GetAllProvidersFormatter.format_serializer_errors)
)
