import requests
from DBL.config import *
from DBL.api_keygen import api_key
from DBL.forms import convert_field_for_db
import DBL.renderer as renderer
from DBL.tags_worker import add_opportunity_tags


def create_provider(provider_name: str) -> int:
    dbl_log(f'Creating provider with name "{provider_name}"')
    headers = {
        "api_key": api_key
    }
    json = {
        "name": provider_name
    }
    response = requests.post('/api/private/opportunity-provider', headers=headers, json=json)
    if response:
        return response.json().get('opportunity_provider_id', -1)
    return -1


def load_md_desc(opp_id, opportunity):
    dbl_log(f'Loading MD DESC to "{opportunity['name']}"')
    renderer.save_md(opportunity, TEMP_MD_DESC_FILE_PATH)

    headers = {
        "api_key": api_key,
        "opportunity_id": opp_id
    }
    files = {
        "description": open(TEMP_MD_DESC_FILE_PATH, 'rb')
    }
    response = requests.patch('/api/private/opportunity/description', headers=headers, files=files)
    return bool(response)


def create_opportunity(opportunity) -> int:
    provider_id = create_provider(opportunity['provider'])  # TODO: provider identify?
    if provider_id < 0:
        dbl_err(f'Can not create provider for opportunity {opportunity["name"]}')
        return -1

    dbl_log(f'Creating opportunity with name "{opportunity['name']}"')
    headers = {
        "api_key": api_key
    }
    json = {
        "name": opportunity['name'],
        "link": opportunity['link'],
        "provider_id": provider_id
    }
    if 'form' in opportunity:
        json['fields'] = {
            "form_link": opportunity['form_link'],
            "fields": [convert_field_for_db(name, field) for name, field in opportunity['form'].items()]
        }
    # Send
    response = requests.post('/api/private/opportunity', headers=headers, json=json)

    if not response:
        dbl_err(f'Can not create opportunity "{opportunity["name"]}" record')
        return -1
    opp_id = response.json().get('opportunity_id', -1)
    if opp_id == -1:
        dbl_err(f'Can not create opportunity "{opportunity["name"]}" record')
        return -1
    
    # Load desc in MD format
    success = load_md_desc(opp_id, opportunity)
    if not success:
        dbl_err(f'Can not add opportunity "{opportunity["name"]}" description MD')
        return -1

    # Load tags
    success = add_opportunity_tags(opp_id, opportunity['tags'])
    if not success:
        dbl_err(f'Can not add opportunity "{opportunity["name"]}" tags')
        return -1

    dbl_log(f'Opportunity "{opportunity["name"]}" successfully created!')
    return 0
