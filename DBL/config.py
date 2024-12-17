import logging

_dbl_logger = logging.getLogger('DBL')


def dbl_log(mes: str):
    _dbl_logger.log(logging.INFO, mes)


def dbl_err(mes: str):
    _dbl_logger.error(mes)


PARSER_JSON_DIR = "DBL/json"
TEMP_MD_DESC_FILE_PATH = "DBL/rendered/dbl_rendered_.md"


OPPORTUNITY_FILTER_MODEL = {
    'link': {
        'required': True,
        'types_supported': [str]
    },
    'form_link': {
        'required': False,
        'types_supported': [str]
    },
    'name': {
        'required': True,
        'types_supported': [str]
    },
    'description': {
        'required': True,
        'types_supported': [str]
    },
    'short_description': {
        'required': True,
        'types_supported': [str]
    },
    # TODO: provider, logo
    'requirements': {
        'required': False,
        'types_supported': [list, str],
        '__list_item_type__': [str]
    },
    'advantages': {
        'required': False,
        'types_supported': [list, str],
        '__list_item_type__': [str]
    },
    'target': {
        'required': False,
        'types_supported': [list, str],
        '__list_item_type__': [str]
    },
    'discipline': {
        'required': False,
        'types_supported': [list, str],
        '__list_item_type__': [str]
    },
    'place': {
        'required': False,
        'types_supported': [list, str],
        '__list_item_type__': [str]
    },
    'period_of_internship': {
        'required': True,
        'types_supported': [str]
    },
    'selection_stages': {
        'required': False,
        'types_supported': [list],
        '__list_item_type__': [dict],
        '__dict__item__struct__': ['name', 'period', 'objectives']
    },
    'allowance': {
        'required': False,
        'types_supported': [str]
    },
    'expenses': {
        'required': False,
        'types_supported': [str]
    },
    'additional': {
        'required': False,
        'types_supported': [list],
        '__list_item_type__': [dict],
        '__dict__item__struct__': ['title', 'description']
    },
    'tags': {
        'required': False,
        'types_supported': [list],
        '__list_item_type__': [str]
    },
    'form': {
        'required': False,
        'types_supported': [dict]  # Free
    }
}