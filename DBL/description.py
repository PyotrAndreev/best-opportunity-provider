from .config import *
from .utils import *
from . import api

from .renderer import save_md


def update_description_md(opportunity: dict, opportunity_id: int) -> bool:
    """
    Updates the description (in Markdown format) of an opportunity in the database.

    This function generates a Markdown file with the description of the opportunity using the 
    `save_md` function, then uploads the file to the database by making a PUT request.

    Arguments:
        opportunity (dict): A dictionary containing the opportunity data, including its name and description.
        opportunity_id (int): The ID of the opportunity to update in the database.

    Returns:
        bool: `True` if the description was successfully updated in the database, `False` otherwise.
    """

    dbl_log(f'Loading MD DESC to "{opportunity['name']}"')
    save_md(opportunity, TEMP_MD_DESC_FILE_PATH)

    files = {
        "description": ('description.md', open(TEMP_MD_DESC_FILE_PATH, 'rb'), 'text/markdown')
    }
    request = api.update_description_md_request(opportunity_id, files)
    return bool(request)
