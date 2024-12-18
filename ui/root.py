from .base import *


@app.get('/')
def root(request: Request, api_key: Annotated[str | None, Cookie()] = None):
    if api_key is None:
        return templates.TemplateResponse(request, 'landing.html')
    if not db.serializers.assert_api_key(api_key):
        return RedirectResponse('/cookies')
    with db.Session.begin() as session:
        personal_api_key = mw.get_personal_api_key(session, api_key)
        if personal_api_key is None:
            return RedirectResponse('/cookies')
        context = { 'user': get_user_dict(personal_api_key.user) }
    return templates.TemplateResponse(request, 'root.html', context=context)
