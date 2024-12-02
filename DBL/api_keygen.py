from db import *

with Session().begin() as session:
    api_key = DeveloperAPIKey.generate(session).key
