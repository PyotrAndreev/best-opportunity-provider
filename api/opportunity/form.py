from .base import *

from copy import copy


class GetOpportunityFormQueryParameters(BaseModel):
    model_config = {'extra': 'ignore'}

    opportunity_id: db.serializers.Id

class GetOpportunityFormFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=fmt.BaseSerializerErrorAppender(
            opportunity_id=fmt.append_serializer_field_error_factory(
                fmt.transform_id_error_factory('Opportunity id')),
        ),
        cookie=fmt.APISerializerErrorAppender(),
    )

@app.get('/api/opportunity/form')
def get_opportunity_form(
    query: Annotated[GetOpportunityFormQueryParameters, Query()],
    cookie: Annotated[db.serializers.APIKeyModel, Cookie()],
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_OPPORTUNITY_ID = 200

    with db.Session.begin() as session:
        api_key = mw.get_personal_api_key_or_error(session, cookie.api_key)
        if not isinstance(api_key, db.PersonalAPIKey):
            return JSONResponse(api_key, status_code=422)
        opportunity = mw.get_opportunity_by_id(
            session, query.opportunity_id, error_code=ErrorCode.INVALID_OPPORTUNITY_ID
        )
        if not isinstance(opportunity, db.Opportunity):
            return JSONResponse(opportunity, status_code=422)
        form = opportunity.get_form()
        if form is None:
            return JSONResponse({})
        reponse = {
            'fields': form.get_dict(),
            'already_responded': query.opportunity_id in map(lambda r: r.opportunity_id, api_key.user.responses),
        }
    return JSONResponse(reponse)
        

RequestValidationErrorHandler.register_handler(
    '/api/opportunity/form', HttpMethod.GET,
    default_request_validation_error_handler_factory(GetOpportunityFormFormatter.format_serializer_errors)
)


class UpdateOpportunityFormSubmitMethod(BaseModel):
    model_config = {'extra': 'ignore'}

    submit_method: db.serializers.OpportunityForm.SubmitMethod

YandexFormsSubmitMethodErrorAppender = fmt.BaseSerializerErrorAppender(
    url=fmt.append_serializer_field_error_factory(fmt.transform_http_url_error_factory('Form URL')),
)

class UpdateOpportunityFormSubmitMethodFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=QueryParametersAppender,
        body=fmt.BaseSerializerErrorAppender(
            submit_method=fmt.TaggedUnionSerializerErrorAppender(
                __root__=fmt.transform_tagged_union_error_factory('Submit method'),
                yandex_forms=YandexFormsSubmitMethodErrorAppender,
            ),
        ),
    )

    @classmethod
    def get_opportunity_form_doesnt_exist_error(*, error_code: int) -> fmt.ErrorTrace:
        return {
            'opportunity_id': [{
                'type': error_code,
                'message': 'Opportunity with provided id doesn\'t have a submit form'
            }],
        }

@app.put('/api/private/opportunity/form/submit')
def update_opportunity_form_submit_method(
    query: Annotated[QueryParameters, Query()],
    body: UpdateOpportunityFormSubmitMethod,
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_OPPORTUNITY_ID = 200
        OPPORTUNITY_FORM_DOESNT_EXIST = 201

    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        opportunity = mw.get_opportunity_by_id(
            session, query.opportunty_id, error_code=ErrorCode.INVALID_OPPORTUNITY_ID
        )
        if not isinstance(opportunity, db.Opportunity):
            return JSONResponse(opportunity, status_code=422)
        if not opportunity.has_form:
            return JSONResponse(
                UpdateOpportunityFormSubmitMethodFormatter.get_opportunity_form_doesnt_exist_error(
                    error_code=ErrorCode.OPPORTUNITY_FORM_DOESNT_EXIST
                ),
                status_code=422
            )
        assert (form := opportunity.get_form()) is not None
        form.update_submit_method(body.submit_method)
    return JSONResponse({})

RequestValidationErrorHandler.register_handler(
    '/api/private/opportunity/form/submit', HttpMethod.PUT,
    default_request_validation_error_handler_factory(
        UpdateOpportunityFormSubmitMethodFormatter.format_serializer_errors)
)


class FieldErrorAppender(fmt.BaseSerializerErrorAppender):
    def __init__(self, **kwargs: fmt.SerializerErrorAppender):
        super().__init__(**kwargs)
        self.label = fmt.append_serializer_field_error_factory(fmt.transform_str_error_factory('Label'))
        self.is_required = fmt.append_serializer_field_error_factory(fmt.transform_bool_error_factory('Is required'))

StringFieldErrorAppender = FieldErrorAppender(
    max_length=fmt.append_serializer_field_error_factory(fmt.transform_int_error_factory('Max length', ge=1)),
)

def __transform_regex_error(error: fmt.PydanticError, _root: int) -> fmt.FormattedError | None:
    match error['type']:
        case 'missing':
            return fmt.FieldErrorCode.MISSING, 'Missing required field'
        case 'string_type':
            return fmt.FieldErrorCode.WRONG_TYPE, 'Regex must be a string'
        case 'pattern_error':
            return fmt.FieldErrorCode.INVALID_PATTERN, 'Regex must be a valid regular expression'

RegexFieldErrorAppender = copy(StringFieldErrorAppender).update(
    regex=fmt.append_serializer_field_error_factory(__transform_regex_error),
)

ChoiceFieldErrorAppender = FieldErrorAppender(
    choices=fmt.append_serializer_list_error_factory(
        transformer=fmt.transform_list_error_factory('Choices', min_length=1),
        element_error_appender=fmt.append_serializer_field_error_factory(
            fmt.transform_str_error_factory('Choice name'))
    ),
)

class UpdateOpportunityFormFields(BaseModel):
    model_config = {'extra': 'ignore'}

    fields: Annotated[db.serializers.OpportunityForm.Fields, Field(min_length=1)]

class UpdateOpportunityFormFieldsFormatter(fmt.BaseSerializerFormatter):
    serializer_error_appender = fmt.RootSerializerErrorAppender(
        query=QueryParametersAppender,
        body=fmt.BaseSerializerErrorAppender(
            fields=fmt.append_serializer_dict_error_factory(
                transformer=fmt.transform_dict_error_factory('Form fields', min_length=1),
                element_error_appender=fmt.TaggedUnionSerializerErrorAppender(
                    __root__=fmt.transform_tagged_union_error_factory('Form field'),
                    string=StringFieldErrorAppender,
                    regex=RegexFieldErrorAppender,
                    choice=ChoiceFieldErrorAppender,
                )
            ),
        ),
    )

@app.put('/api/private/opportunity/form/fields')
def update_opportunity_form_fields(
    query: Annotated[QueryParameters, Query()],
    body: UpdateOpportunityFormFields,
) -> JSONResponse:
    class ErrorCode(IntEnum):
        INVALID_OPPORTUNITY_ID = 200

    with db.Session.begin() as session:
        api_key = mw.get_developer_api_key_or_error(session, query.api_key)
        if not isinstance(api_key, db.DeveloperAPIKey):
            return JSONResponse(api_key, status_code=422)
        opportunity = mw.get_opportunity_by_id(
            session, query.opportunity_id, error_code=ErrorCode.INVALID_OPPORTUNITY_ID
        )
        if not isinstance(opportunity, db.Opportunity):
            return JSONResponse(opportunity, status_code=422)
        if (form := opportunity.get_form()) is None:
            db.OpportunityForm.create(opportunity=opportunity, fields=body.fields)
            opportunity.has_form = True
        else:
            form.update_fields(body.fields)
    return JSONResponse({})

RequestValidationErrorHandler.register_handler(
    '/api/private/opportunity/form/fields', HttpMethod.PUT,
    default_request_validation_error_handler_factory(UpdateOpportunityFormFieldsFormatter.format_serializer_errors)
)
