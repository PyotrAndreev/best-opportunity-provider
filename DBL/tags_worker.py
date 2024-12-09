import requests
import json
from DBL.config import *
from DBL.api_keygen import api_key


TAGS_LIST_PATH = 'DBL/tags/tags_list.txt'
TAGS_JSON_PATH = 'DBL/tags/session_tags_info.json'
TAGS_MAP = None


def load_tag_to_db(tag_name):
    headers = {
        "api_key": api_key
    }
    json = {
        "name": tag_name
    }
    response = requests.post('/api/private/opportunity-tag', headers=headers, json=json)
    if response:
        return response.json().get('tag_id', -1)  # TODO: key naming
    return -1


def update_tags():
    # Get DB tags
    headers = {
        "api_key": api_key
    }
    response = requests.get('/api/private/opportunity-tag/list', headers=headers)
    if not response:
        dbl_err(f'Can not load tags from DB')
    tags_in_db = [(tag['id'], tag['name']) for tag in response.json().get('tags', [])]
    # Get tags from file
    with open(TAGS_LIST_PATH) as f:
        tags_in_list = {i for i in map(lambda x: x.rstrip('\n'), f.readlines()) if i}
    # Load not loaded tags
    not_loaded_tags = tags_in_list.difference({i[1] for i in tags_in_db})
    for tag_name in not_loaded_tags:
        tag_id = load_tag_to_db(tag_name)
        if tag_id == -1:
            dbl_err(f'Error creating tag "{tag_name}"')
            continue
        tags_in_db += [(tag_id, tag_name)]
    # Make session json
    session_json = [{'id': tag[0], 'name': tag[1]} for tag in tags_in_db]
    with open(TAGS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(session_json, f)
    # Saving in global
    global TAGS_MAP
    TAGS_MAP = {tag[1]: tag[0] for tag in tags_in_db}
    # Logging
    dbl_log(f'Tags updated. See: {TAGS_JSON_PATH}')


def add_opportunity_tags(opp_id: int, tag_list: list[str]) -> bool:
    dbl_log(f'Adding tags to opportunity with id={opp_id}')
    # Make tag ids list
    tag_ids = []
    for tag_name in tag_list:
        tag_id = TAGS_MAP.get(tag_name, -1)
        if tag_id == -1:
            dbl_err(f'Tag with name "{tag_name}" not found in DB')
            continue
        tag_ids += [tag_id]
    tag_ids.sort()
    # Update tags
    headers = {
        "api_key": api_key,
        "opportunity_id": opp_id
    }
    json = {
        "tag_ids": tag_ids
    }
    response = requests.put('/api/private/opportunity/tags', headers=headers, json=json)
    return bool(response)
