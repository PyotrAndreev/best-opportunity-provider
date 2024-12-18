from ..base import *

from copy import copy


class Filter(db.serializers.Opportunity.Filter):
    responded: Annotated[bool, Field(default=False)]

FilterErrorAppender = fmt.BaseSerializerErrorAppender(
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
    responded=fmt.append_serializer_field_error_factory(
        fmt.transform_bool_error_factory('Responded')),
)

class GetOpportunityCardPagesFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=FilterErrorAppender,
        cookie=fmt.APISerializerErrorAppender(),
    )

@app.get('/api/opportunity-cards/pages')
def get_opportunity_card_pages(
    query: Annotated[Filter, Query()],
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        filter = mw.validate_filter(session, query)
        if not isinstance(filter, mw.Filter):
            return JSONResponse(filter, status_code=422)
        pages = db.Opportunity.filter_pages(
            session,
            providers=filter.providers,
            tags=filter.tags,
            geotags=filter.geotags,
            user=(api_key.user if query.responded else None),
            public=True,
        )
        return JSONResponse({ 'pages': pages })

RequestValidationErrorHandler.register_handler(
    '/api/opportunity-cards/pages', HttpMethod.GET,
    default_request_validation_error_handler_factory(
        GetOpportunityCardPagesFormatter.format_serializer_errors)
)


class GetOpportunityCardsQueryParameters(Filter):
    page: Annotated[int, Field(default=1, ge=1)]

class GetOpportunityCardsFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=copy(FilterErrorAppender).update(
            page=fmt.append_serializer_field_error_factory(fmt.transform_int_error_factory('Page', ge=1)),
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
