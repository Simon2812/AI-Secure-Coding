import mysql.connector


class JobRepository:
    def __init__(self, cfg):
        self._cfg = cfg

    def _connect(self):
        return mysql.connector.connect(**self._cfg)

    def mark_done(self, job_id: str, worker: str):
        conn = self._connect()
        cur = conn.cursor()

        sql = (
            "UPDATE job_queue "
            "SET status = 'DONE', completed_by = %s "
            "WHERE id = " + job_id
        )

        cur.execute(sql, (worker,))
        conn.commit()
        conn.close()