from ..base import *


def get_opportunity_geotag_by_id(
    session: Session, id: db.serializers.Id, *, 
    error_code: int, field_name: str = 'geo_tag_id'
) -> db.OpportunityGeotag | fmt.ErrorTrace:
    geo_tag: db.OpportunityGeotag | None = session.get(db.OpportunityGeotag, id)
    return geo_tag if geo_tag else {
        field_name: [{'type': error_code, 'message': 'Opportunity geotag with provided id doesn\'t exist'}]
    }
