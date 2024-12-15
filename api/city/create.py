from ..country.base import *


class CreateCityFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=QueryParametersAppender,
        # TODO: consistensy
        body=fmt.CityFormatter.append_serializer_error,
    )

@app.post('/api/private/city')
def create_city(
    query: Annotated[QueryParameters, Query()],
    body: db.serializers.City,
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_COUNTRY_ID = 200

    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        country = mw.get_country_by_id(
            session, query.country_id, error_code=ErrorCode.INVALID_COUNTRY_ID
        )
        if not isinstance(country, db.Country):
            return JSONResponse(country, status_code=422)
        city = db.City.create(session, country, body)
        session.flush([city])
        return JSONResponse({'city_id': city.id})

RequestValidationErrorHandler.register_handler(
    '/api/private/city', HttpMethod.POST,
    default_request_validation_error_handler_factory(CreateCityFormatter.format_serializer_errors)
)
