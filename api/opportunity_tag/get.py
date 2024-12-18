from ..base import *


class GetAllOpportunityTagsFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        cookie=fmt.APISerializerErrorAppender(),
    )

@app.get('/api/opportunity-tag/all')
async def get_all_opportunity_tags(
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        return JSONResponse(db.OpportunityTag.get_all(session))

RequestValidationErrorHandler.register_handler(
    '/api/opportunity-tag/all', HttpMethod.GET,
    default_request_validation_error_handler_factory(GetAllOpportunityTagsFormatter.format_serializer_errors)
)
