from .config import *
from .utils import *
from .api import *

from .description import update_description_md
from .form import update_opportunity_form
from .provider import get_provider_id_by_name
from .tags import update_opportunity_tags


def find_opportunity_by_link(opportunity: dict) -> int:
    """
    Finds an opportunity by its link and returns the associated opportunity ID.

    Args:
        opportunity (dict): A dictionary containing the 'link' of the opportunity.

    Returns:
        int: The opportunity ID if found, otherwise -1.
    """

    json = {
        "link": opportunity['link']
    }
    response = requests.post(f'{HOST}/api/private/opportunity?api_key={api_key}', json=json)

    if not response:
        return -1
    opp_id = response.json().get('opportunity_id', -1)
    return opp_id


def update_opportunity(opportunity: dict, opportunity_id: int) -> bool:
    """
    Updates the opportunity record with the given opportunity ID by updating its form, description, and tags.

    Args:
        opportunity (dict): A dictionary containing the opportunity details to be updated.
        opportunity_id (int): The ID of the opportunity to update.

    Returns:
        bool: True if all updates were successful, otherwise False.
    """

    full_success = True
    dbl_log(f'Updating opportunity with id "{opportunity_id}"')

    # Update form
    success = update_opportunity_form(opportunity, opportunity_id)
    if not success:
        full_success = False

    # Update desc in MD format
    success = update_description_md(opportunity, opportunity_id)
    if not success:
        full_success = False

    # Update tags
    success = update_opportunity_tags(opportunity.get('tags', []), opportunity_id)
    if not success:
        full_success = False

    return full_success


def create_opportunity_main_record(opportunity: dict, provider_id: int) -> int:
    """
    Creates the main record for an opportunity.

    Args:
        opportunity (dict): A dictionary containing the details of the opportunity.
        provider_id (int): The ID of the provider associated with the opportunity.

    Returns:
        int: The created opportunity ID if successful, otherwise -1.
    """

    dbl_log(f'Creating opportunity main record with name "{opportunity['name']}"')
    json = {
        "name": opportunity['name'],
        "link": opportunity['link'],
        "provider_id": provider_id
    }
    response = requests.post(f'{HOST}/api/private/opportunity?api_key={api_key}', json=json)

    if not response:
        dbl_err(f'Can not create opportunity "{opportunity["name"]}" record. See more: {response.json()}')
        return -1
    return response.json()['opportunity_id']


def create_opportunity_card(opportunity: dict, opportunity_id: int) -> bool:
    """
    Creates a card for the opportunity after the main record has been created.

    Args:
        opportunity (dict): A dictionary containing the opportunity details.
        opportunity_id (int): The ID of the opportunity for which the card should be created.

    Returns:
        bool: True if the card was created successfully, otherwise False.
    """

    json = {
        "title": opportunity['name']
    }
    response = requests.post(f'{HOST}/api/private/opportunity-card?api_key={api_key}&opportunity_id={opportunity_id}', json=json)

    if not response:
        dbl_err(f'Can not create opportunity "{opportunity["name"]}" CARD record')
        return False
    return True


def create_opportunity(opportunity: dict) -> bool:
    """
    Creates an opportunity by creating the main record, card, and updating its form, description, and tags.

    Args:
        opportunity (dict): A dictionary containing all the details required to create an opportunity.

    Returns:
        bool: True if all creation steps were successful, otherwise False.
    """

    full_success = True

    # Provider
    provider_id = get_provider_id_by_name(opportunity['provider'])
    if provider_id < 0:
        return False

    # Main record
    opportunity_id = create_opportunity_main_record(opportunity, provider_id)
    if opportunity_id < 0:
        return False

    # Card
    if not create_opportunity_card(opportunity, opportunity_id):
        full_success = False

    # Form
    if not update_opportunity_form(opportunity, opportunity_id):
        full_success = False

    # Description
    if not update_description_md(opportunity, opportunity_id):
        full_success = False

    # Load tags
    if not update_opportunity_tags(opportunity.get('tags', []), opportunity_id):
        full_success = False

    return full_success
