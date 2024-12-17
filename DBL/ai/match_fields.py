from typing import Dict

from .query import query
from .config import *

from json import loads

from enum import IntEnum


class FillType(IntEnum):
    NAME = 0
    SURNAME = 1
    FULLNAME = 2
    EMAIL = 3
    PHONE_NUMBER = 4
    CV = 5
    GPA = 6
    DIPLOMA = 7
    RECOMMENDATIONAL_LETTER = 8
    PASSPORT = 9


def match_fill_type(tp: str) -> FillType:
    return {
        "name": FillType.NAME,
        "surname": FillType.SURNAME,
        "fullname": FillType.FULLNAME,
        "email": FillType.EMAIL,
        "telephone": FillType.PHONE_NUMBER,
        "cv_file": FillType.CV,
        "GPA_file": FillType.GPA,
        "diploma_file": FillType.DIPLOMA,
        "recomendation_letter_file": FillType.RECOMMENDATIONAL_LETTER,
        "passport_scan": FillType.PASSPORT
    }.get(tp, FillType.NAME)


def make_match_fields_query(form_fields: dict):
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
    # ======= EXAMPLE =======
    # Имя (name)
    # Телефон (tel)
    # Электронная почта (email)
    # Дата рождения (birth_day)
    # Резюме (cv)
    # Мотивационное письмо (motivation_letter)
    return query


# Returns combinations of answers that the AI ​​can return
def make_ai_field_classes(form_fields: dict) -> tuple:
    return ((name, label, f"{label} ({name})") for name, label in form_fields.items())


def define_field_class(ai_field_classes: tuple, current_value: str):
    for field_class in ai_field_classes:
        if current_value in field_class:
            return field_class[0]  # returns name
    return None  # Not found


def parse_query_result(result: str, form_fields: dict, json_fname: str) -> dict:
    ai_field_classes = make_ai_field_classes(form_fields)
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
            return {}
        # parsed[key] = attached_class
        parsed[attached_class] = key
    return parsed


def save_ai_result_json(result: str) -> str:
    fname = make_ai_query_result_fname()
    with open(fname, 'w') as f:
        f.write(result)
    return fname


def match_fields(form_fields: Dict[str, str]) -> dict:
    result = query(make_match_fields_query(form_fields))
    fname = save_ai_result_json(result)
    matched = parse_query_result(result, form_fields, fname)
    return matched
