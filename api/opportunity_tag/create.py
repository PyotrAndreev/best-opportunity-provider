from ..base import *


class CreateOpportunityTagFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.APISerializerErrorAppender(),
        body=fmt.BaseSerializerErrorAppender(
            name=fmt.append_serializer_field_error_factory(
                fmt.transform_str_error_factory('Opportunity tag name', min_length=1, max_length=50)
            ),
        ),
    )

@app.post('/api/private/opportunity-tag')
def create_opportunity_tag(
    query: Annotated[db.serializers.APIKeyModel, Query()],
    body: db.serializers.OpportunityTag.Create,
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        tag = mw.create_opportunity_tag(session, body)
        if not isinstance(tag, db.OpportunityTag):
            return JSONResponse(tag, status_code=422)
        session.flush([tag])
        return JSONResponse({'tag_id': tag.id})

RequestValidationErrorHandler.register_handler(
    '/api/private/opportunity-tag', HttpMethod.POST,
    default_request_validation_error_handler_factory(CreateOpportunityTagFormatter.format_serializer_errors)
)
