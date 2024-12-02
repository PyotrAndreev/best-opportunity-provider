from db import *

api_key = None


def generate_api_key():
    global api_key
    with Session().begin() as session:
        api_key = DeveloperAPIKey.generate(session).key
