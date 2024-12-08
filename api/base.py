from typing import Annotated, Callable, Iterable
from enum import IntEnum

from config import (
    app, RequestValidationError, RequestValidationErrorHandler, HttpMethod,
)
import format as fmt
import offer_db as db
import middleware as mw

from fastapi.requests import Request
from fastapi.responses import JSONResponse


def default_request_validation_error_handler_factory(
    formatter: Callable[[Iterable[fmt.PydanticError]], fmt.ErrorTrace],
) -> RequestValidationErrorHandler:
    def handler_fn(error: RequestValidationError) -> JSONResponse:
        return JSONResponse(formatter(error.errors()), status_code=422)

    return handler_fn
