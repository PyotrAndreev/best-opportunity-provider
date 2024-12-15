from ..base import *

from offer_db.models.opportunity.form import (
    FieldErrorCode, FieldError
)


class CreateOpportunityResponseFormatter:
    @classmethod
    def get_opportunity_no_form_error(cls, field_name: str, error_code: int) -> fmt.ErrorTrace:
        return {field_name: [{'type': error_code, 'message': 'Provided opportunity has no submit form'}]}

    @classmethod
    def get_already_responded_error(cls, field_name: str, error_code: int) -> fmt.ErrorTrace:
        return {field_name: [{'type': error_code, 'message': 'Can\'t respond to same opportunity twice'}]}

    @classmethod
    def format_db_errors(cls, errors: list[FieldError]) -> fmt.ErrorTrace:
        formatted_errors: fmt.ErrorTrace = {}
        for error in errors:
            field_name = error.context['field_name']
            if field_name not in formatted_errors:
                formatted_errors[field_name] = []
            formatted_errors[field_name].append({
                'type': error.error_code, 'message': error.error_message
            })
        return formatted_errors

# TODO: docstring
def create_opportunity_response(
    session: Session, user: db.User,
    opportunity: db.Opportunity, data: dict[str, Any],
) -> db.OpportunityResponse | fmt.ErrorTrace:
    class ErrorCode(IntEnum):
        NO_OPPORTUNITY_FORM = 201
        ALREADY_RESPONDED = 202

    form = opportunity.get_form()
    if form is None:
        return CreateOpportunityResponseFormatter.get_opportunity_no_form_error(
            field_name='opportunity_id', error_code=ErrorCode.NO_OPPORTUNITY_FORM
        )
    if opportunity.id in map(lambda r: r.opportunity_id, user.responses):
        return CreateOpportunityResponseFormatter.get_already_responded_error(
            field_name='opportunity_id', error_code=ErrorCode.ALREADY_RESPONDED
        )
    response = db.OpportunityResponse.create(session, user, opportunity, form, data)
    if not isinstance(response, db.OpportunityResponse):
        return CreateOpportunityResponseFormatter.format_db_errors(response)
    # TODO: call submit method
    return response
