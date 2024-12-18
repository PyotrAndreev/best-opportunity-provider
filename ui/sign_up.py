from .base import *


@app.get('/sign-up')
def sign_up(request: Request, api_key: Annotated[str | None, Cookie()] = None):
    if api_key is not None:
        return RedirectResponse('/')
    return templates.TemplateResponse(request, 'sign-up.html')
