import logging
from random import choices

_uff_logger = logging.getLogger('UserFormFiller')


def uff_log(mes: str):
    _uff_logger.log(logging.INFO, mes)


def uff_err(mes: str):
    _uff_logger.error(mes)


AI_QUERY_JSON_DIR = "DBL/ai/json"

from .api_key import OPEN_AI_API_KEY


def make_ai_query_result_fname() -> str:
    RANDOM_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
    uid = ''.join(choices(RANDOM_ALPHABET, k=10))
    return f"{AI_QUERY_JSON_DIR}/ai_qr_{uid}.json"
