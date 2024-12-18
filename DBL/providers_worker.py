import requests
from DBL.config import *
from DBL.api_keygen import api_key

# TODO: fix
HOST = 'http://93.175.4.197:8000'


PROVIDERS_MAP = None


def get_provider_id(provider_name):
    provider_id = PROVIDERS_MAP.get(provider_name, -1)
    if provider_id != -1:
        return provider_id
    return load_provider_to_db(provider_name)


def load_provider_to_db(provider_name):
    json = {
        "name": provider_name
    }
    response = requests.post(f'{HOST}/api/private/opportunity-provider?api_key={api_key}', json=json)
    if response:
        provider_id = response.json().get('provider_id', -1)
        global PROVIDERS_MAP
        PROVIDERS_MAP[provider_name] = provider_id
        return provider_id
    return -1


def update_providers():
    # Get DB providers
    response = requests.get(f'{HOST}/api/private/opportunity-provider/all?api_key={api_key}')
    if not response:
        dbl_err(f'Can not load providers from DB')
    providers_in_db = [(int(i), j) for i, j in response.json().items()]
    # Saving in global
    global PROVIDERS_MAP
    PROVIDERS_MAP = {provider[1]: provider[0] for provider in providers_in_db}
    # Logging
    dbl_log(f'Providers loaded')
