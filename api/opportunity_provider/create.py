from ..base import *


class CreateOpportunityProviderFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.APISerializerErrorAppender(),
        body=fmt.BaseSerializerErrorAppender(
            name=fmt.append_serializer_field_error_factory(
                fmt.transform_str_error_factory('Name')),
        ),
    )

@app.post('/api/private/opportunity-provider')
def create_opportunity_provider(
    query: Annotated[db.serializers.APIKeyModel, Query()],
    body: db.serializers.OpportunityProvider.Create,
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        provider = db.OpportunityProvider.create(session, body)
        session.flush([provider])
        return JSONResponse({'provider_id': provider.id})

RequestValidationErrorHandler.register_handler(
    '/api/private/opportunity-provider', HttpMethod.POST,
    default_request_validation_error_handler_factory(CreateOpportunityProviderFormatter.format_serializer_errors)
)
