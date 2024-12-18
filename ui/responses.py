from .base import *
from api.opportunity_card.filter import GetOpportunityCardsQueryParameters

import json


@app.get('/me/responses')
def responses(
    request: Request,
    filters: Annotated[GetOpportunityCardsQueryParameters,
                       Query(default_factory=GetOpportunityCardsQueryParameters)],
    api_key: Annotated[str | None, Cookie()] = None,
):
    if api_key is None:
        return RedirectResponse('/sign-in')
    if not db.serializers.assert_api_key(api_key):
        return RedirectResponse('/cookies')
    with db.Session.begin() as session:
        personal_api_key = mw.get_personal_api_key(session, api_key)
        if personal_api_key is None:
            return RedirectResponse('/cookies')
        _filters = mw.validate_filter(session, filters)
        if not isinstance(_filters, mw.Filter):
            return RedirectResponse('/me/responses')
        context = {
            'user': get_user_dict(personal_api_key.user),
            'filters': _filters.get_dict(),
        }
        context['filters']['pages'] = db.Opportunity.filter_pages(
            session,
            providers=_filters.providers,
            tags=_filters.tags,
            geotags=_filters.geotags,
            user=personal_api_key.user,
        )
    for key, value in context['filters'].items():
        context['filters'][key] = json.dumps(value)
    context['filters']['page'] = filters.page
    return templates.TemplateResponse(request, 'responses.html', context=context)
