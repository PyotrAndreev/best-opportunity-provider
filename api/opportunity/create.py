from ..base import *


class CreateOpportunityFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.APISerializerErrorAppender(),
        body=fmt.BaseSerializerErrorAppender(
            name=fmt.append_serializer_field_error_factory(
                fmt.transform_str_error_factory('Opportunity name', min_length=1, max_length=50)
            ),
            link=fmt.append_serializer_field_error_factory(
                fmt.transform_http_url_error_factory('Opportunity link', max_length=120)
            ),
            provider_id=fmt.append_serializer_field_error_factory(fmt.transform_id_error_factory('Provider id')),
        ),
    )

@app.post('/api/private/opportunity')
def create_opportunity(
    query: Annotated[db.serializers.APIKeyModel, Query()],
    body: db.serializers.Opportunity.Create,
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_PROVIDER_ID = 200

    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        provider = mw.get_opportunity_provider_by_id(
            session, body.provider_id, error_code=ErrorCode.INVALID_PROVIDER_ID
        )
        if not isinstance(provider, db.OpportunityProvider):
            return JSONResponse(provider, status_code=422)
        opportunity = db.Opportunity.create(session, provider, body)
        session.flush([opportunity])
        return JSONResponse({'opportunity_id': opportunity.id})

RequestValidationErrorHandler.register_handler(
    '/api/private/opportunity', HttpMethod.POST,
    default_request_validation_error_handler_factory(CreateOpportunityFormatter.format_serializer_errors)
)
