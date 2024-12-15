from .base import *


@app.get('/sign-in')
def sign_in(request: Request, api_key: Annotated[str | None, Cookie()] = None):
    if api_key is not None:
        return RedirectResponse('/')
    return templates.TemplateResponse(request, 'sign-in.html')
