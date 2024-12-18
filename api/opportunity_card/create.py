from ..base import *
from ..opportunity.base import QueryParameters, QueryParametersAppender


class CreateOpportunityCardFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=QueryParametersAppender,
        body=fmt.BaseSerializerErrorAppender(
            title=fmt.append_serializer_field_error_factory(
                fmt.transform_str_error_factory('Title', min_length=1, max_length=100)),
            subtitle=fmt.append_serializer_field_error_factory(
                fmt.transform_str_error_factory('Subtitle', min_length=1, max_length=50)),
        ),
    )

@app.post('/api/private/opportunity-card')
def create_opportunity_card(
    query: Annotated[QueryParameters, Query()],
    body: db.serializers.OpportunityCard.Create,
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_OPPORTUNITY_ID = 200

    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        opportunity = mw.get_opportunity_by_id(
            session, query.opportunity_id, error_code=ErrorCode.INVALID_OPPORTUNITY_ID
        )
        if not isinstance(opportunity, db.Opportunity):
            return JSONResponse(opportunity, status_code=422)
        card = db.OpportunityCard.create(session, opportunity, body)
        session.flush([card])
        return JSONResponse({'card_id': card.id})

RequestValidationErrorHandler.register_handler(
    '/api/private/opportunity-card', HttpMethod.POST,
    default_request_validation_error_handler_factory(CreateOpportunityCardFormatter.format_serializer_errors)
)
