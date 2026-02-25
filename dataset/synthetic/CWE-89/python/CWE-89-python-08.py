import psycopg2

def load_jobs(job_ids):
    conn = psycopg2.connect(dbname="queue", user="queue_user", password="queue_pass", host="localhost")
    cur = conn.cursor()

    id_blob = ",".join(job_ids)
    fetch_stmt = "SELECT id, state FROM jobs WHERE id IN (" + id_blob + ")"
    cur.execute(fetch_stmt)
    rows = cur.fetchall()

    conn.close()
    return rows