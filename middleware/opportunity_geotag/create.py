from ..base import *


class CreateOpportunityGeotagFormatter(fmt.BaseDBFormatter):
    class ErrorCode(IntEnum):
        NON_UNIQUE_CITY = 201

    @staticmethod
    def transform_non_unique_city_error(*_) -> fmt.FormattedError:
        return CreateOpportunityGeotagFormatter.ErrorCode.NON_UNIQUE_CITY, 'Geotag with provided city id already exists'

    db_error_appender = fmt.BaseDBErrorAppender({
        db.models.CreateOpportunityGeotagErrorCode.NON_UNIQUE_CITY:
            fmt.append_db_field_error_factory('city_id', transformer=transform_non_unique_city_error),
    })

# TODO: docstring
def create_opportunity_geotag(
    session: Session, city: db.City,
) -> db.OpportunityGeotag | fmt.ErrorTrace:
    geotag = db.OpportunityGeotag.create(session, city)
    if not isinstance(geotag, db.OpportunityGeotag):
        return CreateOpportunityGeotagFormatter.format_db_errors([geotag])
    return geotag
