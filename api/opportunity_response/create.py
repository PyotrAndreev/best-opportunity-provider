from ..base import *

from typing import Any


class CreateOpportunityResponseQueryParameters(BaseModel):
    model_config = {'extra': 'ignore'}

    opportunity_id: db.serializers.Id

class CreateOpportunityResponseBody(BaseModel):
    model_config = {'extra': 'ignore'}

    reponse_data: dict[str, Any]

class CreateOpportunityResponseFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.BaseSerializerErrorAppender(
            opportunity_id=fmt.append_serializer_field_error_factory(
                fmt.transform_id_error_factory('Opportunity id')),
        ),
        body=fmt.BaseSerializerErrorAppender(
            # Child elements can't cause errors, so do not use `append_serializer_dict_field_error_factory`
            response_data=fmt.append_serializer_field_error_factory(
                fmt.transform_dict_error_factory('Reponse data')),
        ),
        cookie=fmt.APISerializerErrorAppender(),
    )

@app.post('/api/opportunity-response')
async def create_opportunity_response(
    query: Annotated[CreateOpportunityResponseQueryParameters, Query()],
    body: CreateOpportunityResponseBody,
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_OPPORTUNITY_ID = 200

    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        opportunity = mw.get_opportunity_by_id(
            session, query.opportunity_id, error_code=ErrorCode.INVALID_OPPORTUNITY_ID
        )
        if not isinstance(opportunity, db.Opportunity):
            return JSONResponse(opportunity, status_code=422)
        response = mw.create_opportunity_response(
            session, api_key.user, opportunity, body.reponse_data
        )
        if not isinstance(response, db.OpportunityResponse):
            session.rollback()
            return JSONResponse(response, status_code=422)
    return JSONResponse({})

RequestValidationErrorHandler.register_handler(
    '/api/opportunity-response', HttpMethod.POST,
    default_request_validation_error_handler_factory(
        CreateOpportunityResponseFormatter.format_serializer_errors)
)
