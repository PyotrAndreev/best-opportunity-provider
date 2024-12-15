from ..base import *


class CreateCountryFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.APISerializerErrorAppender,
        # TODO: consistensy
        body=fmt.CountryFormatter.append_serializer_error,
    )

@app.post('/api/private/country')
def create_country(
    query: Annotated[db.serializers.APIKeyModel, Query()],
    body: db.serializers.Country,
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        country = mw.create_country(session, body)
        if not isinstance(country, db.Country):
            return JSONResponse(country, status_code=422)
        session.flush([country])
        return JSONResponse({'country_id': country.id})

RequestValidationErrorHandler.register_handler(
    '/api/private/country', HttpMethod.POST,
    default_request_validation_error_handler_factory(CreateCountryFormatter.format_serializer_errors)
)
