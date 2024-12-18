from ..base import *


class CreateCountryFormatter(fmt.BaseDBFormatter):
    class ErrorCode(IntEnum):
        NON_UNIQUE_NAME = 200

    @staticmethod
    def transform_non_unique_name_error(*_) -> fmt.FormattedError:
        return CreateCountryFormatter.ErrorCode.NON_UNIQUE_NAME, 'Country with given name already exists'

    db_error_appender = fmt.BaseDBErrorAppender({
        db.models.CreateCountryErrorCode.NON_UNIQUE_NAME:
            fmt.append_db_field_error_factory('name', transformer=transform_non_unique_name_error),
    })

def create_country(
    session: Session, fields: db.serializers.Country
) -> db.Country | fmt.ErrorTrace:
    country = db.Country.create(session, fields)
    if not isinstance(country, db.Country):
        return CreateCountryFormatter.format_db_errors([country])
    return country
