from importlib import import_module
from time import sleep
from DBL.config import *

PARSERS = [
    'example_maker',
    'parser_Changellenge',
    'parser_Habr',
    'parser_InternationalStudent',
    'parser_Studyqa',
    'parser_Superjob',
    'parser_Yandex'
]

PARSER_TIMEOUT = 5.0


def parse_file(parser_name) -> str:
    try:
        parser_module = import_module(f'DBL.parsers.{parser_name}')
        return parser_module.run()
    except Exception as ex:
        dbl_err(f'Thrown exception while parsing module "{parser_name}". Ex: {ex}')
        return None


def parse_all_opportunities() -> list[str]:
    json_names = []
    for parser_name in PARSERS:
        sleep(PARSER_TIMEOUT)
        t = parse_file(parser_name)
        if t is None:
            dbl_err(f'Can not parse module {parser_name}')
            continue
        json_names += [t]
        dbl_log(f'Parsed module "{parser_name}"')
    return json_names
