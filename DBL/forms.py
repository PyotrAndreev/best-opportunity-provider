from .field_matcher import add_form_fill


def form_type(field: dict) -> dict:
    tp = field['type']
    """
    if tp == 'number':
        return {"type": "regex", "regex": "^[0-9]*$"}
    """
    if tp == 'number':
        return {"type": "number", "le": field['min'], "ge": field['max']}
    if tp == 'email':
        return {"type": "regex", "regex": r"^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$"}
    if tp == 'choice':
        return {"type": "choice", "choices": field['choices']}
    if tp == 'file':
        return {"type": "file", "max_size_byte": field['max_size_byte']}  # TODO: file
    # text
    return {"type": "string", "max_length": field["max_len"]}


def convert_field_for_db(field) -> dict:
    res = {
            'label': field['label'],
            'is_required': field['required']
    }
    res.update(form_type(field))
    return res


def convert_fields_for_db(opportunity: dict):
    opportunity['form'] = {name: convert_field_for_db(field) for name, field in opportunity['form'].items()}
    add_form_fill(opportunity['form'])
