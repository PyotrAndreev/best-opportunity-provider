from .base import *

import re
import json


def opportunity_doesnt_exist(request: Request):
    return templates.TemplateResponse(request, 'opportunity404.html', status_code=404)

@app.get('/opportunity/{opportunity_id}')
def opportunity(
    request: Request,
    opportunity_id: Annotated[int, Path(ge=1)],
    api_key: Annotated[str | None, Cookie()] = None,
):
    class ErrorCode(IntEnum):
        INVALID_OPPORTUNITY_ID = 200

    if api_key is None:
        return RedirectResponse('/sign-in')
    if not db.serializers.assert_api_key(api_key):
        return RedirectResponse('/cookies')
    with db.Session.begin() as session:
        personal_api_key = mw.get_personal_api_key(session, api_key)
        if personal_api_key is None:
            return RedirectResponse('/cookies')
        opportunity = mw.get_opportunity_by_id(
            session, opportunity_id, error_code=ErrorCode.INVALID_OPPORTUNITY_ID
        )
        if not isinstance(opportunity, db.Opportunity):
            return opportunity_doesnt_exist(request)
        context = {
            'user': get_user_dict(personal_api_key.user),
            'opportunity_dump': json.dumps(opportunity.get_dict()),
        }
    return templates.TemplateResponse(request, 'opportunity.html', context=context)

RequestValidationErrorHandler.register_pattern_handler(
    re.compile('/opportunity*'), [HttpMethod.GET],
    lambda r, _e: opportunity_doesnt_exist(r)
)
