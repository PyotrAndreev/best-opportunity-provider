from DBL.api_keygen import generate_api_key
from DBL.tags_worker import update_tags
from DBL.updater import update


def init_dbl():  # TODO: Call in start up
    generate_api_key()
    update_tags()