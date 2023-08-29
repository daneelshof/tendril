from fastapi import FastAPI
import redis
from rq import Queue
import time
from database import Postgres
from models import Run

api = FastAPI()
pg = Postgres()

redis_connection = redis.Redis(host='redis', port=6379)
rq = Queue(connection=redis_connection)


@api.get("/health")
async def get_health():
    return {"healthy": "true"}


@api.get("/queue/test")
async def test_queue():
    task = rq.enqueue('worker.tasks.get_random')
    time.sleep(0.100)
    return task.return_value()


@api.get("/runs")
async def get_test_runs():
    return pg.get_all_test_runs()


@api.post("/run")
async def start_new_run(run: Run):
    run_id = pg.insert_new_test_run(run.name, 'PENDING')
    task = rq.enqueue('worker.tasks.run_test', run_id)
    pg.update_test_run_status(run_id, 'QUEUED')
    return run_id
