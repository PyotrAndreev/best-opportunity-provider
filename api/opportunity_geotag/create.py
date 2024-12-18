from ..base import *


class CreateOpportunityGeotagFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.APISerializerErrorAppender(),
        body=fmt.BaseSerializerErrorAppender(
            city_id=fmt.append_serializer_field_error_factory(fmt.transform_id_error_factory('City id')),
        ),
    )

@app.post('/api/private/opportunity-geotag')
def create_opportunity_geotag(
    query: Annotated[db.serializers.APIKeyModel, Query()],
    body: db.serializers.OpportunityGeoTag.Create,
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_CITY_ID = 200

    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        city = mw.get_city_by_id(
            session, body.city_id, error_code=ErrorCode.INVALID_CITY_ID
        )
        if not isinstance(city, db.City):
            return JSONResponse(city, status_code=422)
        geotag = mw.create_opportunity_geotag(session, city)
        if not isinstance(geotag, db.OpportunityGeotag):
            return JSONResponse(geotag, status_code=422)
        session.flush([geotag])
        return JSONResponse({'geotag_id': geotag.id})

RequestValidationErrorHandler.register_handler(
    '/api/private/opportunity-geotag', HttpMethod.POST,
    default_request_validation_error_handler_factory(CreateOpportunityGeotagFormatter.format_serializer_errors)
)
