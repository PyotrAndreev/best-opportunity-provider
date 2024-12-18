from .provider import update_providers
from .tags import update_tags

from .updater import update

def init_dbl():
    update_tags()
    update_providers()


# For run all parsers & update DB: run update() function
