from DBL.config import PARSER_JSON_DIR


JSON = """
[
    {
        "link": "https://google.com",
        "form_link": "https://google.com/form",

        "name": "Стажировка уборщиком в Балаклаве",
        "short_description": "Получите незабываемый опыт, работая уборщиков в лучшем месте Крымского полуострова",
        "description": "Эта стажировка — шанс получить опыт работы в сфере гостиничного и ресторанного бизнеса и провести время в Балаклеве. Размещение происходит в отелях 4 и 5 звезд в отелях курортной зоны. Выбор вакансий зависит от уровня подготовки кандидата. Так вы сможете улучшить навыки работы в сфере обслуживания. Все вакансии предполагают нагрузку в 35 рабочих часов в неделю с 1 или 2 днями выходных — абсолютно фиксированный график. Вы за несколько месяцев вперед узнаете обо всех последних днях, которые вы можете смело посвятить путешествиям. Однако такие условия фиксации распространяются и на заработную плату, поэтому лучше не рассчитывать на возможность получения дополнительного дохода сверх установленной суммы стипендии.Если же вы предпочитаете проживание в кемпингах, это напрямую влияет на ваш доход — будьте готовы к сверхнормативной работе, однако она компенсируется более высоким уровнем дохода (как минимум в полтора-два раза выше установленной стипендии).В свободное время изучайте местные традиции и наслаждайтесь экзотическими пейзажами Балаклавы.",
        "provider": "Google LTD",
        "logo": "logos/balaclava.png",

        "requirements_for_applicant": ["Хорошее знание английского (B2+)", "Умение работать в команде", "Опыт C++ 70+ лет"],
        "advantages_of_internship": ["Получение опыта в работе с людьми, в том числе и иностранцами", "Сертификат об окончании для личного портфолио"],
        "who_is_the_internship_intended_for": ["Студенты бакалавриата", "Студенты магистратуры", "Аспиранты"],
        "discipline": ["Computer Science", "Гостиничное дело"],

        "place": ["Балаклава"],
        "period_of_internship": "С 01.07.2077 до 31.07.2077",

        "selection_stages": [
            {"stage_name": "Подача", "stage_period": "01.04.2077 - 01.05.2077", "objectives": ["Подача CV", "Подача мотивационного письма"]},
            {"stage_name": "Одобрение CV и собеседование", "stage_period": "01.05.2077 - 01.06.2077", "objectives": ["Одобрение CV", "Собеседование с дирекцией"]},
            {"stage_name": "Список прошедших", "stage_period": "01.06.2077 - 07.06.2077", "objectives": []}
        ],

        "allowance": "50.000 руб за весь период",
        "expenses": "10 руб./день на курорный сбор",

        "additional_information": [
            {"title_of_section": "Про нашу Балаклаву", "section": "Наша Балаклава славится тем-то тем-то"},
            {"title_of_section": "Бесплатное размещение", "section": "Мы предлагаем услуги бесплатного размещения в нашем же отеле"},
            {"title_of_section": "Перелет на наш счет", "section": "Мы полностью возместим расходы на перелет"}
        ],

        "tags": ["accomondation", "transportation", "insurance"],

        "form": {
            "name": {
                "type": "string",
                "required": true,
                "label": "Имя (латиницей)",
                "max_len": 100
            },
            "email": {
                "type": "email",
                "required": true,
                "name": "Ваш email"
            },
            "age": {
                "type": "number",
                "required": true,
                "name": "Ваш возраст на момент начала стажировки",
                "min": 18,
                "max": 30
            },
            "lang_lvl": {
                "type": "choice",
                "required": true,
                "name": "Ваш уровень владения английским",
                "choices": ["B2", "C1", "C2", "L1 ДИЯ"]
            },
            "cv": {
                "type": "file",
                "required": true,
                "name": "Отправьте свое резюме",
                "max_size_byte": 10485760
            },
            "telephone": {
                "type": "tel",
                "required": true,
                "name": "Ваш телефон"
            }
        }
    }
]
"""


def run():
    # Fake parser
    with open(f'{PARSER_JSON_DIR}/example_run.json', 'w', encoding='utf-8') as f:
        f.write(JSON)
    return 'example_run.json'
