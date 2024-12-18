from typing import Dict
from json import loads

from .config import *
from .utils import *
from .query import query

from match_fill_type import match_fill_type


def make_match_fields_query(form_fields: dict):
    """
    Constructs a query to request the AI to match form field labels with predefined field names in JSON format.

    Args:
        form_fields (dict): A dictionary where keys are field names and values are field labels.

    Returns:
        str: A formatted query string to be used in the AI request, asking for the mapping of form field labels to field names.
    """

    query = """
Пожалуйста, добавь название каждого поля формы ниже в соответствующую ему ячейку JSON.
Вот структура, которой ты должен следовать (если в JSON что-то останется несопоставленным, то оставь ячейку пустой):

{
  "name": "",
  "surname": "",
  "fullname",
  "email": "",
  "telephone": "",
  "cv_file": "",
  "GPA_file": "",
  "diploma_file": "",
  "recomendation_letter_file": "",
  "passport_scan": "",
}

Не добавляй никакого дополнительного текста перед или после JSON.

Вот список полей формы:

"""
    query += "\n".join([f"{label} ({name})" for name, label in form_fields.items()])
    return query


# Returns combinations of answers that the AI ​​can return
def make_field_classes_for_ai(form_fields: dict) -> tuple:
    """
    Creates combinations of field names, field labels, and a concatenated string for AI processing.

    Args:
        form_fields (dict): A dictionary where keys are field names and values are field labels.

    Returns:
        tuple: A tuple of tuples, where each inner tuple contains (field name, field label, concatenated label and name).
    """

    return ((name, label, f"{label} ({name})") for name, label in form_fields.items())


def define_field_class(ai_field_classes: tuple, current_value: str):
    """
    Defines the field class by matching the current value to the corresponding AI field class.

    Args:
        ai_field_classes (tuple): A tuple of tuples, where each inner tuple represents a field class (name, label, concatenated string).
        current_value (str): The current value (label or text) to be matched to a field class.

    Returns:
        str: The field name (key) if a match is found, otherwise None.
    """

    for field_class in ai_field_classes:
        if current_value in field_class:
            return field_class[0]  # returns name
    return None  # Not found


def save_ai_result_json(result: str) -> str:
    """
    Saves the AI result (JSON string) to a file.

    Args:
        result (str): The AI result as a JSON string.

    Returns:
        str: The filename where the result was saved.
    """

    fname = make_ai_query_result_fname()
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(result)
    return fname


def serialize_query_result(result: str, form_fields: dict, json_fname: str) -> dict:
    """
    Parses the AI result JSON string, maps the values to the appropriate field names, and returns a dictionary.

    Args:
        result (str): The raw JSON result from the AI.
        form_fields (dict): A dictionary of form fields where keys are field names and values are field labels.
        json_fname (str): The name of the file where the AI result was saved.

    Returns:
        dict: A dictionary mapping field names to the corresponding JSON key if a valid match is found, otherwise an empty dictionary.
    """

    ai_field_classes = make_field_classes_for_ai(form_fields)
    try:
        json_result = loads(result)
    except Exception as ex:
        uff_err(f'Error while parsing AI result ({ex}). Checkout file {json_fname}')
        return {}
    parsed = {}
    for key, value in json_result.items():
        if not value:
            continue
        attached_class = define_field_class(ai_field_classes, value)
        if not attached_class:
            uff_err(f'Error while defining class of "{key}: {value}". Checkout file {json_fname}')
            continue
        parsed[attached_class] = key
    return parsed


def match_fields(form_fields: Dict[str, str]) -> dict:
    """
    Matches form fields with predefined field names by querying the AI and processing the result.

    Args:
        form_fields (dict): A dictionary where keys are field names and values are field labels.

    Returns:
        dict: A dictionary where keys are form field names and values are matched field names from the AI result.
    """

    query_result = query(make_match_fields_query(form_fields))
    json_file_name = save_ai_result_json(query_result)
    matched = serialize_query_result(query_result, form_fields, json_file_name)
    return matched


def add_form_fillers(fields: dict):
    """
    Adds the 'fill' attribute to each form field by matching the field's label to its corresponding field type.

    Args:
        fields (dict): A dictionary of form fields, where each field is a dictionary containing its attributes.
    """

    relationship_table = match_fields({name: field['label'] for name, field in fields.items()})
    for field_name, db_rel in relationship_table.items():
        fields[field_name]['fill'] = match_fill_type(db_rel)  # adds fill attribute to every form unit
