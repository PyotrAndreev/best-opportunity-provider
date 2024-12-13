from userform.ai import match_fields

example = {
    "name": "Имя",
    "tel": "Телефон",
    "email": "Электронная почта",
    "birth_day": "Дата рождения",
    "cv": "Резюме",
    "motivation_letter": "Мотивационное письмо"
}

print(match_fields(example))
