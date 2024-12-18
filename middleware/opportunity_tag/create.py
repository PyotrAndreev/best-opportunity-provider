from ..base import *


class CreateOpportunityTagFormatter(fmt.BaseDBFormatter):
    class ErrorCode(IntEnum):
        NON_UNIQUE_NAME = 200

    @staticmethod
    def transform_non_unique_name_error(*_) -> fmt.FormattedError:
        return CreateOpportunityTagFormatter.ErrorCode.NON_UNIQUE_NAME, 'Tag with provided name already exists'

    db_error_appender = fmt.BaseDBErrorAppender({
        db.models.CreateOpportunityTagErrorCode.NON_UNIQUE_NAME:
            fmt.append_db_field_error_factory('name', transformer=transform_non_unique_name_error),
    })

# TODO: docstring
def create_opportunity_tag(
    session: Session, fields: db.serializers.OpportunityTag.Create,
) -> db.OpportunityTag | fmt.ErrorTrace:
    tag = db.OpportunityTag.create(session, fields)
    if not isinstance(tag, db.OpportunityTag):
        return CreateOpportunityTagFormatter.format_db_errors([tag])
    return tag
