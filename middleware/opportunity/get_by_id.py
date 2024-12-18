from ..base import *


def get_opportunity_by_id(
    session: Session, id: db.serializers.Id, *, 
    error_code: int, field_name: str = 'opportunity_id'
) -> db.Opportunity | fmt.ErrorTrace:
    opportunity: db.Opportunity | None = session.get(db.Opportunity, id)
    return opportunity if opportunity else {
        field_name: [{'type': error_code, 'message': 'Opportunity with provided id doesn\'t exist'}]
    }
