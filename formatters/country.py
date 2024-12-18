from .base import *


class CountryFormatter(BaseSerializerFormatter):
    serializer_error_appender = BaseSerializerErrorAppender(
        name=append_serializer_field_error_factory(
            transform_str_error_factory('Country name', min_length=1, max_length=50)),
        phone_code=append_serializer_field_error_factory(
            transform_int_error_factory('Phone code', ge=1, le=999)),
    )
