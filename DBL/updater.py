from DBL.config import *
import DBL.json_worker as json_worker
from DBL.parsers.run import parse_all
import DBL.api_worker as api_worker


def get_opportunities_list():
    names = parse_all()
    opportunities = []
    for json_fname in names:
        opportunities += json_worker.parse_opportunity_json(json_fname)
    return opportunities


def update():
    opportunities = get_opportunities_list()
    dbl_log('Loading opportunities to DB')
    success = 0
    for opp in opportunities:
        result = api_worker.create_opportunity(opp)
        if result == 0:
            success += 1
    dbl_log(f'Loaded opportunities to DB ({success}/{len(opportunities)})')
