import random
import time
import requests
import logging
from database import Postgres

pg = Postgres()


def run_test(run_id):
    logging.debug(f'Starting run_test for {run_id}')

    pg.update_test_run_status(run_id, 'RUNNING')
    time.sleep(random.randint(1,6))

    url = 'https://api.ipify.org/?format=json'
    req = requests.get(url)
    logging.debug(f'Completed web request: {req.text}')

    pg.update_test_run_result(run_id, req.text)
    pg.update_test_run_status(run_id, 'DONE')
    logging.debug(f'Completed run_test for {run_id}')

    return True
