from ..base import *


class GetOpportunityCardsQueryParameters(db.serializers.Opportunity.Filter):
    responded: Annotated[bool, Field(default=False)]

class GetOpportunityCardsFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.BaseSerializerErrorAppender(
            provider_ids=fmt.append_serializer_list_error_factory(
                transformer=fmt.transform_list_error_factory('Provider ids'),
                element_error_appender=fmt.append_serializer_field_error_factory(
                    fmt.transform_id_error_factory('Provider id'))
            ),
            tag_ids=fmt.append_serializer_list_error_factory(
                transformer=fmt.transform_list_error_factory('Tag ids'),
                element_error_appender=fmt.append_serializer_field_error_factory(
                    fmt.transform_id_error_factory('Tag id'))
            ),
            geotag_ids=fmt.append_serializer_list_error_factory(
                transformer=fmt.transform_list_error_factory('Geotag ids'),
                element_error_appender=fmt.append_serializer_field_error_factory(
                    fmt.transform_id_error_factory('Geotag id'))
            ),
            page=fmt.append_serializer_field_error_factory(fmt.transform_int_error_factory('Page', ge=1)),
            responded=fmt.append_serializer_field_error_factory(fmt.transform_bool_error_factory('Responded')),
        ),
        cookie=fmt.APISerializerErrorAppender(),
    )

@app.get('/api/opportunity-cards')
def get_opportunity_cards(
    query: Annotated[GetOpportunityCardsQueryParameters, Query()],
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        filter = mw.validate_filter(session, query)
        if not isinstance(filter, mw.Filter):
            return JSONResponse(filter, status_code=422)
        opportunities = db.Opportunity.filter(
            session,
            providers=filter.providers,
            tags=filter.tags,
            geotags=filter.geotags,
            page=query.page,
            user=(api_key.user if query.responded else None),
            public=True,
        )
        response = [opportunity.cards[0].get_dict() for opportunity in opportunities]
    return JSONResponse(response)

RequestValidationErrorHandler.register_handler(
    '/api/opportunity-cards', HttpMethod.GET,
    default_request_validation_error_handler_factory(GetOpportunityCardsFormatter.format_serializer_errors)
)
