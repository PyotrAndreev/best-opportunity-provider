from ..base import *


class QueryParameters(BaseModel):
    model_config = {'extra': 'ignore'}

    api_key: db.serializers.APIKey
    user_id: db.serializers.Id


QueryParametersAppender = fmt.APISerializerErrorAppender(
    user_id=fmt.append_serializer_field_error_factory(fmt.transform_id_error_factory('User id')),
)
