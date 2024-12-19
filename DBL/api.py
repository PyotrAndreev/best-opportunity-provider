import requests

from .config import *
from .utils import *


def update_description_md_request(opportunity_id: int, files: dict) -> requests.Request:
    response = requests.put(
        f'{HOST}/api/private/opportunity/description?api_key={API_KEY}&opportunity_id={opportunity_id}', files=files
    )
    return response


def update_opportunity_form_fields_request(opportunity: dict, opportunity_id: int) -> requests.Request:
    json = {
        "fields": opportunity['form']
    }
    response = requests.put(f'{HOST}/api/private/opportunity/form/fields?api_key={API_KEY}&opportunity_id={opportunity_id}', json=json)
    return response


def update_opportunity_form_submit_method_request(opportunity: dict, opportunity_id: int) -> requests.Request:
    json = {
        "url": opportunity['form_link']
    }
    response = requests.put(f'{HOST}/api/private/opportunity/form/submit?api_key={API_KEY}&opportunity_id={opportunity_id}', json=json)
    return response


def find_opportunity_by_link_request(link: str) -> requests.Request:
    json = {
        "link": link
    }
    # TODO: Misha must to realize it
    response = requests.post(f'{HOST}/api/private/opportunity?api_key={API_KEY}', json=json)

    if not response:
        return -1
    return response.json()['opportunity_id']


def create_opportunity_main_record_request(opportunity: dict, provider_id: int) -> requests.Request:
    json = {
        "name": opportunity['name'],
        "link": opportunity['link'],
        "provider_id": provider_id
    }
    response = requests.post(f'{HOST}/api/private/opportunity?api_key={API_KEY}', json=json)
    return response


def create_opportunity_card_request(opportunity: dict, opportunity_id: int) -> requests.Request:
    json = {
        "title": opportunity['name']
    }
    response = requests.post(f'{HOST}/api/private/opportunity-card?api_key={API_KEY}&opportunity_id={opportunity_id}', json=json)
    return response


def get_all_providers_request() -> requests.Response:
    response = requests.get(f'{HOST}/api/private/opportunity-provider/all?api_key={API_KEY}')
    return response


def create_provider_request(provider_name: str) -> requests.Response:
    json = {
        "name": provider_name
    }
    response = requests.post(f'{HOST}/api/private/opportunity-provider?api_key={API_KEY}', json=json)
    return response


def create_tag_request(tag_name: str) -> requests.Response:
    json = {
        "name": tag_name
    }
    response = requests.post(f'{HOST}/api/private/opportunity-tag?api_key={API_KEY}', json=json)
    return response


def get_all_tags_request() -> requests.Response:
    response = requests.get(f'{HOST}/api/private/opportunity-tag/all?api_key={API_KEY}')
    return response


def update_opportunity_tags_request(opportunity_id: int, tag_ids: list[int]) -> requests.Response:
    json = {
        "tag_ids": tag_ids
    }
    # TODO: Musha must change method on PUT
    response = requests.post(f'{HOST}/api/private/opportunity/tags?api_key={API_KEY}&opportunity_id={opportunity_id}', json=json)
    return response
