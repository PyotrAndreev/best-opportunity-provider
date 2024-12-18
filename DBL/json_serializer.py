import json

from .config import *
from .utils import *


def make_json_path(name: str) -> str:
    return f'DBL/json/{name}.json'


def load_json_from_file(name: str) -> Optional[dict]:
    """
    Loads JSON data from a file.

    Attempts to open and load a JSON file with the given name. If successful, it returns
    the loaded data as a dictionary. If the file cannot be opened or parsed, it returns `None`.

    Args:
        name (str): The name of the JSON file to load (without the '.json' extension).

    Returns:
        Optional[dict]: The parsed JSON data if successful, or `None` if there is an error.
    """

    try:
        with open(make_json_path(name), encoding='utf-8') as file:
            data = json.load(file)
            return data
    except Exception as ex:
        return


def remove_dict_keys(dct: dict, keys: list):
    """
    Removes specified keys from a dictionary.

    This function removes the provided list of keys from the given dictionary.

    Args:
        dct (dict): The dictionary from which keys should be removed.
        keys (list): A list of keys to remove from the dictionary.
    """

    for rm_key in keys:
        del dct[rm_key]


def clear_record_empty_fields(opp_record: dict):
    """
    Removes empty fields from an opportunity record.

    This function scans through an opportunity record and removes any key-value pairs
    where the value is considered empty (e.g., `None`, empty string, empty list, etc.).

    Args:
        opp_record (dict): The opportunity record from which empty fields will be removed.
    """

    keys_to_del = []
    for rec_key, rec_value in opp_record.items():
        if not rec_value:  # types in STD: str, dict, list
            keys_to_del += [rec_key]
    # remove empty keys
    remove_dict_keys(opp_record, keys_to_del)


def record_check_by_keys(opp_record: dict, fname, record_index) -> bool:
    """
    Validates an opportunity record by checking its keys and types against a model.

    This function checks if the opportunity record contains all required fields, and that
    the types of the field values match the expected types from a predefined model.
    It also converts certain fields to the correct type (e.g., string to list).

    Args:
        opp_record (dict): The opportunity record to validate.
        fname (str): The name of the JSON file that contains the opportunity records.
        record_index (int): The index of the current record in the file.

    Returns:
        bool: `True` if the record is valid, `False` otherwise.
    """

    not_valid_type_mes = lambda k: f'Opportunity #{record_index + 1} in "{fname}" has not valid type of "{k}" field'

    keys_to_del = []
    models = OPPORTUNITY_FILTER_MODEL.copy()
    for key, value in opp_record.items():
        if key not in models:
            keys_to_del += [key]
            continue
        field_model = models.pop(key)
        field_types = set(field_model['types_supported'])
        # Check for types
        if not any((isinstance(value, tp) for tp in field_types)):
            dbl_err(not_valid_type_mes(key))
            return False
        # Str to list convertation
        if {str, list}.issubset(field_types) and isinstance(value, str):
            opp_record[key] = [value]
        # Check list item types
        if '__list_item_type__' in field_model and isinstance(value, list):
            if not all((any((isinstance(i, j) for j in field_model['__list_item_type__'])) for i in value)):
                dbl_err(not_valid_type_mes(key))
                return False
        # Check dict item types
        if '__dict__item__struct__' in field_model and isinstance(value, dict):
            if set(value.keys()) != set(field_model['__dict__item__struct__']):
                dbl_err(not_valid_type_mes(key))
                return False
    # rm empty keys
    remove_dict_keys(opp_record, keys_to_del)
    # Check remaining models
    req_models = [m_nm for m_nm, m_desc in models.items() if m_desc['required']]
    if req_models:
        dbl_err(f'Opportunity #{record_index} in "{fname}" has not required fields: {", ".join(req_models)}')
        return False
    return True


def filter_opportunity_record(opp_record: dict, fname: str, record_index: int) -> bool:
    """
    Filters and validates an opportunity record.

    This function first checks if the opportunity record is a dictionary. It then clears any empty fields and validates
    the record's keys and types based on a predefined model.

    Args:
        opp_record (dict): The opportunity record to be filtered and validated.
        fname (str): The name of the JSON file that contains the opportunity records.
        record_index (int): The index of the current record in the file.

    Returns:
        bool: `True` if the record passes validation, `False` otherwise.
    """

    if not isinstance(opp_record, dict):
        dbl_err(f'Opportunity #{record_index} in "{fname}" is not a dict instance')
        return False
    # Clear empty fields
    clear_record_empty_fields(opp_record)
    # KeyWorker
    return record_check_by_keys(opp_record, fname, record_index)


def parse_opportunity_json(fname: str) -> Optional[list[dict]]:
    """
    Loads and filters opportunity records from a JSON file.

    This function loads the JSON data from the specified file, validates and filters the opportunity records
    using the `filter_opportunity_record` function, and returns a list of valid opportunity records.

    Args:
        fname (str): The name of the JSON file containing the opportunity records.

    Returns:
        Optional[list[dict]]: A list of valid opportunity records, or `None` if an error occurs.
    """

    # Load
    json_data = load_json_from_file(fname)
    if not json_data:
        dbl_err(f'Can\' parse json file "{fname}"')
        return
    dbl_log(f'Loaded opportunity set file: {fname}')
    # Filter
    if not isinstance(json_data, list):
        dbl_err(f'Json file "{fname}" is not list instance')
        return
    filtered_opp_list = []
    for ind, opp_record in enumerate(json_data):
        if filter_opportunity_record(opp_record, fname, ind):
            filtered_opp_list.append(opp_record)
    dbl_log(f'Filtered opportunity set: {fname}')
    return filtered_opp_list
