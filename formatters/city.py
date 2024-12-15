from .base import *


class CityFormatter(BaseSerializerFormatter):
    serializer_error_appender = BaseSerializerErrorAppender(
        name=append_serializer_field_error_factory(
            transform_str_error_factory('City name', min_length=1, max_length=50)),
    )
