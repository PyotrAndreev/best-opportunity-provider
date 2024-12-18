from .base import *


class DateFormatter(BaseSerializerFormatter):
    class ErrorCode(IntEnum):
        INVALID_DATE = 200

    @staticmethod
    def transform_root_error(error: PydanticError, _root: int) -> FormattedError | None:
        match error['type']:
            case 'missing':
                return FieldErrorCode.MISSING, 'Missing required field'
            case 'model_attributes_type':
                return FieldErrorCode.WRONG_TYPE, 'Date must be a dictionary'
            case 'date_error':
                return DateFormatter.ErrorCode.INVALID_DATE, 'Invalid combination of year, month and day'

    serializer_error_appender = BaseSerializerErrorAppender(
        day=append_serializer_field_error_factory(transform_int_error_factory('Day', ge=1, le=31)),
        month=append_serializer_field_error_factory(transform_int_error_factory('Month', ge=1, le=12)),
        year=append_serializer_field_error_factory(transform_int_error_factory('Year', ge=1900))
    )
