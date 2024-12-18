from .config import *
from .utils import *
from .parsers.run import parse_all_opportunities
from .opportunity_record import find_opportunity_by_link, create_opportunity, update_opportunity
from .json_serializer import parse_opportunity_json


def run_opportunities_parsers() -> list[dict]:
    """
    Runs the parsers to extract opportunities from JSON files and returns a list of parsed opportunities.

    This function calls the `parse_all_opportunities()` to get the list of JSON filenames, then parses each
    JSON file using `parse_opportunity_json()` and collects the results.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents an opportunity.
    """

    json_names = parse_all_opportunities()
    opportunities = []
    for json_fname in json_names:
        if (result := parse_opportunity_json(json_fname)) is None:
            continue
        opportunities += result
    return opportunities


def update():
    """
    Updates the database with new or updated opportunities.

    This function first parses all opportunities using `run_opportunities_parsers()`. Then, for each opportunity, 
    it checks if the opportunity already exists in the database by its link using `find_opportunity_by_link()`.
    - If the opportunity does not exist, it is created using `create_opportunity()`.
    - If the opportunity exists, it is updated using `update_opportunity()`.

    The result of each operation is tracked in a dictionary `worker_r` that keeps count of created, updated, 
    and errored opportunities. A log is generated at the end showing the overall result.

    The function logs the progress of the operation at each step.
    """

    opportunities = run_opportunities_parsers()
    dbl_log('Loading opportunities to DB')
    worker_r = {'created': 0, 'updated': 0, 'err': 0, 'overall': len(opportunities)}
    for opp in opportunities:
        opp_id = find_opportunity_by_link(opp)
        if opp_id == -1:
            success = create_opportunity(opp)
            key = 'created' if success else 'err'
        else:
            success = update_opportunity(opp, opp_id)
            key = 'updated' if success == 0 else 'err'
        worker_r[key] += 1
    dbl_log(f'Loaded opportunities to DB ({worker_r})')
