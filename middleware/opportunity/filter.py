from ..base import *
from offer_db.utils import GenericError

from dataclasses import dataclass


@dataclass
class Filter:
    providers: list[db.OpportunityProvider]
    tags: list[db.OpportunityTag]
    geotags: list[db.OpportunityGeotag]

    def get_providers_dict(self) -> dict[str, str]:
        return {str(provider.id): provider.name for provider in self.providers}

    def get_tags_dict(self) -> dict[str, str]:
        return {str(tag.id): tag.name for tag in self.tags}

    def get_geotags_dict(self) -> dict[str, str]:
        return {str(geotag.id): (geotag.city.country.name, geotag.city.name)
                for geotag in self.geotags}

    def get_dict(self) -> dict[str, Any]:
        return {
            'providers': self.get_providers_dict(),
            'tags': self.get_tags_dict(),
            'geotags': self.get_geotags_dict(),
        }

class ErrorCode(IntEnum):
    INVALID_PROVIDER_ID = 200
    INVALID_TAG_ID = 201
    INVALID_GEOTAG_ID = 202

type Error = GenericError[ErrorCode, int]

class ValidateFilterFormatter(fmt.BaseDBFormatter):
    @staticmethod
    def append_invalid_provider_id_error(error: Error, errors: fmt.ErrorTrace, _) -> None:
        if 'provider_ids' not in errors:
            errors['provider_ids'] = {}
        tag_index = str(error.context)
        if tag_index not in errors['provider_ids']:
            errors['provider_ids'][tag_index] = []
        errors['provider_ids'][tag_index].append({'type': error.error_code, 'message': error.error_message})

    @staticmethod
    def append_invalid_tag_id_error(error: Error, errors: fmt.ErrorTrace, _) -> None:
        if 'tag_ids' not in errors:
            errors['tag_ids'] = {}
        tag_index = str(error.context)
        if tag_index not in errors['tag_ids']:
            errors['tag_ids'][tag_index] = []
        errors['tag_ids'][tag_index].append({'type': error.error_code, 'message': error.error_message})

    @staticmethod
    def append_invalid_geotag_id_error(error: Error, errors: fmt.ErrorTrace, _) -> None:
        if 'geotag_ids' not in errors:
            errors['geotag_ids'] = {}
        tag_index = str(error.context)
        if tag_index not in errors['geotag_ids']:
            errors['geotag_ids'][tag_index] = []
        errors['geotag_ids'][tag_index].append({'type': error.error_code, 'message': error.error_message})

    db_error_appender = fmt.BaseDBErrorAppender({
        ErrorCode.INVALID_PROVIDER_ID: append_invalid_provider_id_error,
        ErrorCode.INVALID_TAG_ID: append_invalid_tag_id_error,
        ErrorCode.INVALID_GEOTAG_ID: append_invalid_geotag_id_error,
    })

def get_error(error_code: ErrorCode, error_message: str, context: int) -> Error:
    return GenericError(
        error_code=error_code,
        error_message=error_message,
        context=context,
    )

# TODO: docstring
def validate_filter(
    session: Session, filter: db.serializers.Opportunity.Filter,
) -> Filter | fmt.ErrorTrace:
    errors: list[Error] = []
    result = Filter(providers=[], tags=[], geotags=[])
    for index, provider_id in enumerate(filter.provider_ids):
        provider: db.OpportunityProvider | None = session.get(db.OpportunityProvider, provider_id)
        if provider is None:
            errors.append(get_error(
                erorr_code=ErrorCode.INVALID_PROVIDER_ID,
                error_message='Provider with given id doesn\'t exist',
                context=index,
            ))
        else:
            result.providers.append(provider)
    for index, tag_id in enumerate(filter.tag_ids):
        tag: db.OpportunityTag | None = session.get(db.OpportunityTag, tag_id)
        if tag is None:
            errors.append(get_error(
                erorr_code=ErrorCode.INVALID_TAG_ID,
                error_message='Opportunity tag with provided id doesn\'t exist',
                context=index,
            ))
        else:
            result.tags.append(tag)
    for index, geotag_id in enumerate(filter.geotag_ids):
        geotag: db.OpportunityGeotag | None = session.get(db.OpportunityGeotag, geotag_id)
        if geotag is None:
            errors.append(get_error(
                error_code=ErrorCode.INVALID_GEOTAG_ID,
                error_message='Opportunity geotag with provided id doesn\'t exist',
                context=index,
            ))
        else:
            result.geotags.append(geotag)
    if len(errors) > 0:
        return ValidateFilterFormatter.format_db_errors(errors)
    return result
    