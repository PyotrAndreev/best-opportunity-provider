import json

from .config import *
from .utils import *
from . import api

TAGS_MAP = {}


def create_tag(tag_name: str) -> int:
    """
    Creates a new tag in the database.

    Sends a POST request to the API to create a tag with the specified name. If the tag is created successfully,
    the tag ID is added to the global `TAGS_MAP` dictionary.

    Args:
        tag_name (str): The name of the tag to be created.

    Returns:
        int: The ID of the created tag if successful, or -1 if the tag creation fails.
    """

    response = api.create_tag_request(tag_name)
    if not response:
        dbl_err(f'Can not create tag "{tag_name}"')
        return -1
    tag_id = response.json()['tag_id']
    TAGS_MAP[tag_name] = tag_id
    return tag_id


def update_tags():
    """
    Updates the list of tags by synchronizing the tags from a file with those stored in the database.

    This function retrieves the existing tags from the database and the tags from the file located at `TAGS_LIST_PATH`.
    It then compares them and creates any tags that are missing from the database. Finally, it writes the updated list of
    tags to a JSON file at `TAGS_JSON_PATH` and updates the global `TAGS_MAP` dictionary to store the mapping of tag names
    to tag IDs.

    Logs the completion of the update process.
    """

    # Get DB tags
    response = api.get_all_tags_request()
    if not response:
        dbl_err(f'Can not load tags from DB')
        return
    tags_in_db = [(int(tag_id), tag_name) for tag_id, tag_name in response.json().items()]
    # Get tags from file
    with open(TAGS_LIST_PATH) as f:
        tags_in_list = {i for i in map(lambda x: x.rstrip('\n'), f.readlines()) if i}
    # Load not loaded tags
    not_loaded_tags = tags_in_list.difference({i[1] for i in tags_in_db})
    for tag_name in not_loaded_tags:
        tag_id = create_tag(tag_name)
        if tag_id != -1:
            tags_in_db += [(tag_id, tag_name)]
    # Make session json
    session_json = [{'id': int(tag[0]), 'name': tag[1]} for tag in tags_in_db]
    with open(TAGS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(session_json, f)
    # Saving in global
    global TAGS_MAP
    TAGS_MAP = {tag[1]: tag[0] for tag in tags_in_db}
    # Logging
    dbl_log(f'Tags updated. See: {TAGS_JSON_PATH}')


def get_tag_id_by_name(tag_name: str) -> int:
    """
    Retrieves the ID of a tag by its name. If the tag is not found in the global `TAGS_MAP`, it creates the tag.

    Args:
        tag_name (str): The name of the tag whose ID is to be retrieved.

    Returns:
        int: The ID of the tag if found in `TAGS_MAP`, or the ID of the newly created tag if not found.
    """

    tag_id = TAGS_MAP.get(tag_name, -1)
    if tag_id != -1:
        return tag_id
    return create_tag(tag_name)


def update_opportunity_tags(tag_list: list[str], opportunity_id: int) -> bool:
    """
    Updates the tags associated with an opportunity.

    This function retrieves the IDs of the tags specified in `tag_list` and associates them with the given opportunity.
    It sends a POST request to the API to update the tags for the opportunity with the specified `opportunity_id`.

    Args:
        tag_list (list[str]): A list of tag names to be associated with the opportunity.
        opportunity_id (int): The ID of the opportunity to update.

    Returns:
        bool: `True` if the tags were successfully updated, otherwise `False`.
    """

    dbl_log(f'Adding tags to opportunity with id={opportunity_id}')
    # Make tag ids list
    tag_ids = []
    for tag_name in tag_list:
        tag_id = get_tag_id_by_name(tag_name)
        if tag_id == -1:
            continue
        tag_ids += [tag_id]
    tag_ids.sort()
    # Update tags
    response = api.update_opportunity_tags_request(opportunity_id, tag_ids)
    return response
