from ..base import *


def get_opportunity_provider_by_id(
    session: Session, id: db.serializers.Id, *, 
    error_code: int, field_name: str = 'provider_id'
) -> db.OpportunityProvider | fmt.ErrorTrace:
    provider: db.OpportunityProvider | None = session.get(db.OpportunityProvider, id)
    return provider if provider else {
        field_name: [{'type': error_code, 'message': 'Opportunity provider with provided id doesn\'t exist'}]
    }
