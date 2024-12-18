from DBL.config import *
import DBL.json_worker as json_worker
from DBL.parsers.run import parse_all
import DBL.api_worker as api_worker


def get_opportunities_list():
    # names = parse_all()
    names = ['allVacancyCard_JSON_Yandex', 'allVacancyCard_JSON_Studyqa']
    opportunities = []
    for json_fname in names:
        if (result := json_worker.parse_opportunity_json(json_fname)) is None:
            continue
        opportunities += result
    return opportunities


def update():
    opportunities = get_opportunities_list()
    dbl_log('Loading opportunities to DB')
    worker_r = {'created': 0, 'updated': 0, 'err': 0, 'overall': len(opportunities)}
    for opp in opportunities:
        # opp_id = api_worker.find_opportunity_by_link(opp)
        opp_id = -1  # TODO: Fuck
        if opp_id < 0:
            result = api_worker.create_opportunity(opp)
            key = 'created' if result == 0 else 'err'
        else:
            result = api_worker.update_opportunity(opp, opp_id)
            key = 'updated' if result == 0 else 'err'
        worker_r[key] += 1
    dbl_log(f'Loaded opportunities to DB ({worker_r})')
