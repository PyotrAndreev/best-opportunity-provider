from ..base import *


class QueryParameters(BaseModel):
    model_config = {'extra': 'ignore'}

    api_key: db.serializers.APIKey
    country_id: db.serializers.Id


QueryParametersAppender = fmt.APISerializerErrorAppender(
    opportunity_id=fmt.append_serializer_field_error_factory(fmt.transform_id_error_factory('Country id')),
)
