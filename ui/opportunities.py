from .base import *

import json


@app.get('/opportunities')
def opportunities(
    request: Request,
    filters: Annotated[db.serializers.Opportunity.Filter,
                       Query(default_factory=db.serializers.Opportunity.Filter)],
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
            return RedirectResponse('/opportunities')
        context = _filters.get_dict()
    for key, value in context.items():
        context[key] = json.dumps(value)
    context['page'] = filters.page
    return templates.TemplateResponse(request, 'opportunities.html', context=context)
