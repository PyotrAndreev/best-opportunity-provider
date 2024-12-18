from ..base import *


def get_country_by_id(
    session: Session, id: db.serializers.Id, *, 
    error_code: int, field_name: str = 'country_id'
) -> db.Country | fmt.ErrorTrace:
    country: db.Country | None = session.get(db.Country, id)
    return country if country else {
        field_name: [{'type': error_code, 'message': 'Country with provided id doesn\'t exist'}]
    }
