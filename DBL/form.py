from .config import *
from .utils import *
from . import api

from . import ai


def serialize_form_type(field: dict) -> dict:
    """
    Serializes the field type into a format suitable for database storage.

    Depending on the field type (e.g., number, email, choice, file), 
    the function creates the corresponding structure for storing in the database.

    Arguments:
        field (dict): A dictionary containing information about the form field 
                      (e.g., field type, min/max values, etc.).

    Returns:
        dict: A serialized dictionary representing the field type for database storage.
    """

    tp = field['type']
    if tp == 'number':
        return {"type": "number", "le": field['min'], "ge": field['max']}
    if tp == 'email':
        return {"type": "regex", "regex": r"^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$"}
    if tp == 'choice':
        return {"type": "choice", "choices": field['choices']}
    if tp == 'file':
        return {"type": "file", "max_size_byte": field['max_size_byte']}
    # text
    return {"type": "string", "max_length": field["max_len"]}


def convert_field_for_db(field) -> dict:
    """
    Converts a form field into a format suitable for database storage.

    This function adds additional attributes (e.g., required flag) to the field 
    and serializes its type using the `serialize_form_type` function.

    Arguments:
        field (dict): A dictionary containing information about the form field 
                      (e.g., label, required flag, field type).

    Returns:
        dict: A dictionary representing the form field in a format suitable for database storage.
    """

    res = {
        'label': field['label'],
        'is_required': field['required']
    }
    res.update(serialize_form_type(field))
    return res


def serialize_fields_for_db(opportunity: dict):
    """
    Serializes all form fields for an opportunity into a format suitable for database storage.

    This function iterates through all form fields in the opportunity and converts each field 
    using the `convert_field_for_db` function. Additionally, AI integration is applied to add 
    extra data to the fields.

    Arguments:
        opportunity (dict): A dictionary containing opportunity data, including the form fields.
    """

    opportunity['form'] = {name: convert_field_for_db(field) for name, field in opportunity['form'].items()}
    # AI integration
    ai.add_form_fillers(opportunity['form'])


def update_opportunity_form_fields(opportunity: dict, opportunity_id: int) -> bool:
    """
    Updates the form fields for an opportunity in the database.

    This function sends a request to update the form fields for a specific opportunity by its ID.

    Arguments:
        opportunity (dict): A dictionary containing opportunity data, including the form fields.
        opportunity_id (int): The ID of the opportunity in the database.

    Returns:
        bool: `True` if the form fields were successfully updated, otherwise `False`.
    """

    response = api.update_opportunity_form_fields_request(opportunity, opportunity_id)

    if not response:
        dbl_err(f'Can not update opportunity (id={opportunity_id}) form')
        return False
    return True


def update_opportunity_form_submit_method(opportunity: dict, opportunity_id: int) -> bool:
    """
    Updates the form submission method for an opportunity in the database.

    This function sends a request to update the URL for the form submission method for a specific opportunity.

    Arguments:
        opportunity (dict): A dictionary containing opportunity data, including the form submission URL.
        opportunity_id (int): The ID of the opportunity in the database.

    Returns:
        bool: `True` if the form submission method was successfully updated, otherwise `False`.
    """

    response = api.update_opportunity_form_submit_method_request(opportunity, opportunity_id)

    if not response:
        dbl_err(f'Can not update opportunity (id={opportunity_id}) form method')
        return False
    return True


def update_opportunity_form(opportunity: dict, opportunity_id: int) -> bool:
    """
    Updates all form fields and the form submission method for an opportunity in the database.

    This function serializes the form fields, updates the fields, and updates the form submission method 
    for a specific opportunity. It returns `True` if all operations are successful.

    Arguments:
        opportunity (dict): A dictionary containing opportunity data, including form fields and form submission URL.
        opportunity_id (int): The ID of the opportunity in the database.

    Returns:
        bool: `True` if all update operations were successful, otherwise `False`.
    """

    full_success = True

    # Serialize
    serialize_fields_for_db(opportunity)

    # Fields
    if not update_opportunity_form_fields(opportunity, opportunity_id):
        full_success = False

    # Submit
    if 'form_link' in opportunity:
        if not update_opportunity_form_submit_method(opportunity, opportunity_id):
            full_success = False

    return full_success
