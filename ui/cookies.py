from .base import *


@app.get('/cookies')
def cookies(request: Request):
    response = templates.TemplateResponse(request, 'cookies.html')
    response.delete_cookie('api_key')
    return response
