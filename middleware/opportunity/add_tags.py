from ..base import *
from ..opportunity_tag.get_by_id import get_opportunity_tag_by_id
from ..opportunity_geotag.get_by_id import get_opportunity_geotag_by_id


def get_invalid_tags_error(errors: list[fmt.ErrorTrace], *, field_name: str) -> fmt.ErrorTrace:
    result = {}
    for error in errors:
        result.update(error)
    return { field_name: result }


class TagsList(BaseModel):
    model_config = {'extra': 'ignore'}

    tag_ids: Annotated[list[db.serializers.Id], Field(min_length=1)]

def add_opportunity_tags(
    session: Session, opportunity: db.Opportunity, tag_ids: TagsList,
    *, error_code: int, field_name: str = 'tag_ids',
) -> None | fmt.ErrorTrace:
    tag_errors: list[fmt.ErrorTrace] = []
    tags: list[db.OpportunityTag] = []
    for id in tag_ids.tag_ids:
        tag = get_opportunity_tag_by_id(session, id, error_code=error_code)
        if isinstance(tag, db.OpportunityTag):
            tags.append(tag)
        else:
            tag_errors.append(tag)
    if len(tag_errors) > 0:
        return get_invalid_tags_error(tag_errors, field_name=field_name)
    opportunity.add_tags(tags)


class GeotagsList(BaseModel):
    model_config = {'extra': 'ignore'}

    geotag_ids: Annotated[list[db.serializers.Id], Field(min_length=1)]

def add_opportunity_geotags(
    session: Session, opportunity: db.Opportunity, tag_ids: GeotagsList,
    *, error_code: int, field_name: str = 'geotag_ids',
) -> None | fmt.ErrorTrace:
    geotag_errors: list[fmt.ErrorTrace] = []
    geotags: list[db.OpportunityGeotag] = []
    for id in tag_ids.geotag_ids:
        geotag = get_opportunity_geotag_by_id(session, id, error_code=error_code)
        if isinstance(geotag, db.OpportunityGeotag):
            geotags.append(geotag)
        else:
            geotag_errors.append(geotag)
    if len(geotag_errors) > 0:
        return get_invalid_tags_error(geotag_errors, field_name=field_name)
    opportunity.add_geotags(geotags)
