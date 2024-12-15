from ..base import *


def get_city_by_id(
    session: Session, id: db.serializers.Id, *, 
    error_code: int, field_name: str = 'city_id'
) -> db.City | fmt.ErrorTrace:
    city: db.City | None = session.get(db.City, id)
    return city if city else {
        field_name: [{'type': error_code, 'message': 'City with provided id doesn\'t exist'}]
    }
