from .config import *
from .utils import *
from .api import *


PROVIDERS_MAP = {}


def update_providers():
    """
    Updates the global `PROVIDERS_MAP` by loading the list of providers from the database.

    This function sends a GET request to retrieve all providers from the database and stores the provider names
    and their corresponding IDs in the global `PROVIDERS_MAP` dictionary. If the request fails, it logs an error.

    The `PROVIDERS_MAP` dictionary is updated with the format:
    {
        provider_name (str): provider_id (int)
    }
    """

    # Get all providers in DB
    response = requests.get(f'{HOST}/api/private/opportunity-provider/all?api_key={api_key}')
    if not response:
        dbl_err(f'Can not load providers from DB')
        return
    # Saving in global
    global PROVIDERS_MAP
    PROVIDERS_MAP = {provider_name: int(provider_id) for provider_id, provider_name in response.json().items()}
    # Logging
    dbl_log(f'Providers loaded')


def create_provider(provider_name: str) -> int:
    """
    Creates a new provider in the database.

    Sends a POST request to the API to create a provider with the specified name. If the provider is created successfully,
    the provider ID is added to the global `PROVIDERS_MAP` dictionary.

    Args:
        provider_name (str): The name of the provider to be created.

    Returns:
        int: The ID of the created provider if successful, or -1 if the provider creation fails.
    """

    json = {
        "name": provider_name
    }
    response = requests.post(f'{HOST}/api/private/opportunity-provider?api_key={api_key}', json=json)
    if not response:
        dbl_err(f'Can not create provider "{provider_name}"')
        return -1
    provider_id = response.json()['provider_id']
    PROVIDERS_MAP[provider_name] = provider_id
    return provider_id


def get_provider_id_by_name(provider_name: str) -> int:
    """
    Retrieves the ID of a provider by its name. If the provider is not found in the global `PROVIDERS_MAP`, it creates the provider.

    This function first checks if the provider exists in the `PROVIDERS_MAP` dictionary. If it does, the corresponding
    provider ID is returned. If not, the function attempts to create the provider and return its ID.

    Args:
        provider_name (str): The name of the provider whose ID is to be retrieved.

    Returns:
        int: The ID of the provider if found in the `PROVIDERS_MAP`, or the ID of the newly created provider if not found.
    """

    provider_id = PROVIDERS_MAP.get(provider_name, -1)
    if provider_id != -1:
        return provider_id
    return create_provider(provider_name)
