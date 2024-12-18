from typing import Annotated, Callable, Iterable
from enum import IntEnum
import re

from config import (
    app, RequestValidationError, RequestValidationErrorHandler, HttpMethod,
)
import formatters as fmt
import offer_db as db
import middleware as mw

from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse

from fastapi import Path, Query, Cookie
from pydantic import BaseModel, Field


def default_request_validation_error_handler_factory(
    formatter: Callable[[Iterable[fmt.PydanticError]], fmt.ErrorTrace],
) -> RequestValidationErrorHandler.Handler:
    def handler_fn(_request: Request, error: RequestValidationError) -> JSONResponse:
        return JSONResponse(formatter(error.errors()), status_code=422)

    return handler_fn
