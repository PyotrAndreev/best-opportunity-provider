from ..base import *


def get_cv_by_id(
    session: Session, id: db.serializers.Id, *, 
    error_code: int, field_name: str = 'cv_id'
) -> db.CV | fmt.ErrorTrace:
    cv: db.CV | None = session.get(db.CV, id)
    return cv if cv else {
        field_name: [{'type': error_code, 'message': 'CV with provided id doesn\'t exist'}]
    }
