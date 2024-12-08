# ===== Logging setup =====

import logging
import os
from datetime import datetime

LOG_FOLDER = datetime.now().strftime('%d.%m.%Y')
LOG_FILENAME = datetime.now().strftime('%H%M%S')

os.makedirs(f'logs/{LOG_FOLDER}', exist_ok=True)
logging.basicConfig(
    filename=f'logs/{LOG_FOLDER}/{LOG_FILENAME}.log',
    format='[%(levelname)s @ %(asctime)s] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

logger = logging.getLogger()


# ===== Application configuration =====

HOST: str = '127.0.0.1'
PORT: int = 8000

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount('/static', StaticFiles(directory='static', html=True), name='static')


from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')


# ===== Request validation error configuration =====

from enum import StrEnum

class HttpMethod(StrEnum):
    GET = 'GET'
    POST = 'POST'

from typing import Callable
import re

from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.exceptions import RequestValidationError

class RequestValidationErrorHandler:
    type Handler = Callable[[RequestValidationError], Response]

    url_to_handler: dict[tuple[str, HttpMethod], Handler] = {}
    url_pattern_to_handler: dict[HttpMethod, list[tuple[re.Pattern, Handler]]] = {}
    default_handler: Handler | None = None

    @classmethod
    def register_handler(cls, url: str, method: HttpMethod, handler: Handler) -> None:
        cls.url_to_handler[(url, method)] = handler

    @classmethod
    def register_pattern_handler(cls, pattern: re.Pattern, method: HttpMethod, handler: Handler) -> None:
        cls.url_pattern_to_handler.setdefault(method, []).append((pattern, handler))

    @classmethod
    def set_default_handler(cls, handler: Handler) -> None:
        cls.default_handler = handler

    @classmethod
    def handle_error(cls, request: Request, error: RequestValidationError) -> Response:
        if handler := cls.url_to_handler.get((request.url.path, request.method.upper())):
            return handler(error)
        if handlers := cls.url_pattern_to_handler.get(request.method.upper()):
            for pattern, handler in handlers:
                if pattern.match(request.url.path):
                    return handler(error)
        logger.debug('Reached default request validation error handler (url=\'%s\', method=%s, error=%s)')
        if cls.default_handler:
            return cls.default_handler(error)
        raise KeyError(f'Unhandled request validation error: {error} '
                       f'(url=\'{request.url.path}\', method={request.method})')


@app.exception_handler(RequestValidationError)
def request_validation_error_handler(request: Request, error: RequestValidationError) -> Response:
    return RequestValidationErrorHandler.handle_error(request, error)
