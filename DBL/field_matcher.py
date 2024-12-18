# from .ai.match_fields import match_fields, match_fill_type
# TODO: add key

def add_form_fill(fields: dict):
    relationship_table = match_fields({name: field['label'] for name, field in fields.items()})
    for field_name, db_rel in relationship_table.items():
        fields[field_name]['fill'] = match_fill_type(db_rel)
