import os
import psycopg2
from base import Monostate

class Postgres(Monostate):

    def __init__(self):
        if not hasattr(self, '_conn'):
            try:
                self._conn = psycopg2.connect(
                    host=os.getenv("POSTGRES_HOST"),
                    dbname=os.getenv("POSTGRES_DB"),
                    user=os.getenv("POSTGRES_USER"),
                    password=os.getenv("POSTGRES_PASSWORD"),
                    port=os.getenv("POSTGRES_PORT")
                )
            except psycopg2.OperationalError as e:
                print(f"Database connection failed: {e}")

    def get_all_test_runs(self):
        cur = self._conn.cursor()
        cur.execute('select * from test_runs;')
        return cur.fetchall()


    def insert_new_test_run(self, name, status):
        cur = self._conn.cursor()
        sql = 'insert into test_runs (name, status) values (%s, %s) returning run_id;'
        cur.execute(sql, (name, status))
        run_id = cur.fetchone()[0]
        self._conn.commit()
        cur.close()
        return run_id


    def update_test_run_status(self, run_id, status):
        cur = self._conn.cursor()
        sql = 'update test_runs set status = %s where run_id = %s;'
        cur.execute(sql, (status, run_id))
        self._conn.commit()
        cur.close()
        return True


    def update_test_run_result(self, run_id, result):
        cur = self._conn.cursor()
        sql = 'update test_runs set result = %s where run_id = %s;'
        cur.execute(sql, (result, run_id))
        self._conn.commit()
        cur.close()
        return True
