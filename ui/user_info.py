from .base import *


@app.get('/me/info')
def user_info(request: Request, api_key: Annotated[str | None, Cookie()] = None):
    if api_key is None:
        return RedirectResponse('/sign-in')
    if not db.serializers.assert_api_key(api_key):
        return RedirectResponse('/cookies')
    with db.Session.begin() as session:
        personal_api_key = mw.get_personal_api_key(session, api_key)
        if personal_api_key is None:
            return RedirectResponse('/cookies')
        context = personal_api_key.user.user_info.get_dict() | {
            'user': get_user_dict(personal_api_key.user),
        }
    return templates.TemplateResponse(request, 'user-info.html', context=context)
