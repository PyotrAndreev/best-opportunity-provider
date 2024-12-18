from ..base import *


def get_opportunity_tag_by_id(
    session: Session, id: db.serializers.Id, *, 
    error_code: int, field_name: str = 'tag_id'
) -> db.OpportunityTag | fmt.ErrorTrace:
    tag: db.OpportunityTag | None = session.get(db.OpportunityTag, id)
    return tag if tag else {
        field_name: [{'type': error_code, 'message': 'Opportunity tag with provided id doesn\'t exist'}]
    }
