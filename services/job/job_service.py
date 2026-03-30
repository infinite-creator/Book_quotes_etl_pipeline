from contextlib import closing
from datetime import datetime

from db.database import get_connection
from pipeline.orchestrator import run_pipeline


def create_job():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO jobs (status, started_at) VALUES (?, ?)
        """, ('running', datetime.utcnow().isoformat()))

        conn.commit()

        return cursor.lastrowid

def update_job_status(job_id, status, error_message=None):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE jobs SET status = ?, finished_at = ?, error_message = ? WHERE id = ?
        """, (status, datetime.utcnow().isoformat(), error_message, job_id))

        conn.commit()

def run_etl_job():
    job_id = create_job()

    try:
        with closing(get_connection()) as conn:
            run_pipeline(conn=conn)

        update_job_status(job_id, 'success')
        
    except Exception as error:
        update_job_status(job_id, 'failed', str(error))
        raise