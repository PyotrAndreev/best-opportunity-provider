from . import (
    user, opportunity, opportunity_provider, 
    opportunity_tag, opportunity_geotag,
    opportunity_card, opportunity_response,
    country, city,
)
from .base import *


def default_api_request_validation_error_handler(_error: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        { 'detail': 'Invalid path parameters for requested API endpoint' },
        status_code=422,
    )

RequestValidationErrorHandler.register_pattern_handler(
    re.compile('/api/*'), list(HttpMethod),
    default_api_request_validation_error_handler
)
