import logging
from random import choices

from .config import *

_uff_logger = logging.getLogger('UserFormFiller')


def uff_log(mes: str):
    _uff_logger.log(logging.INFO, mes)


def uff_err(mes: str):
    _uff_logger.error(mes)


def make_ai_query_result_fname() -> str:
    RANDOM_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
    uid = ''.join(choices(RANDOM_ALPHABET, k=10))
    return f"{AI_QUERY_JSON_DIR}/ai_qr_{uid}.json"
