import random
import time
import requests
from database import Postgres

pg = Postgres()


def get_random():
    return random.randint(0, 100)


def run_test(run_id):
    pg.update_test_run_status(run_id, 'RUNNING')
    time.sleep(random.randint(1,6))
    #url = 'https://api.ipify.org?format=json'
    #req = requests.get(url)
    pg.update_test_run_result(run_id, 'example result')
    pg.update_test_run_status(run_id, 'DONE')
    return True
