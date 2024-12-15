import config
import api, ui
from uvicorn import run


if __name__ == '__main__':
    run('config:app', host=config.HOST, port=config.PORT)
