from .query import query


def make_match_fields_query():
    query = """
Пожалуйста, добавь название каждого поля формы ниже в соответствующую ему ячейку JSON.
Вот структура, которой ты должен следовать (если в JSON что-то останется несопоставленным, то оставь ячейку пустой):

{
  "name": "",
  "telephone": "",
  "email": "",
  "birthday": "",
  "cv_file": "",
  "motivation_letter_file": "",
  "recomendation_letter_file": ""
}

Не добавляй никакого дополнительного текста перед или после JSON.

Вот список полей формы:

Имя (name)
Телефон (tel)
Электронная почта (email)
Дата рождения (birth_day)
Резюме (cv)
Мотивационное письмо (motivation_letter)
"""
    return query


def match_fields(form_fields: dict) -> dict:
    pass
