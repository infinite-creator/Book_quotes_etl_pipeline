from pathlib import Path
import sys

if __package__ in {None, ""}:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

import pandas as pd
import streamlit as st

from book_quotes_etl.db.database import get_connection
from book_quotes_etl.services.job.job_service import run_etl_job


def load_dashboard_data():
    conn = get_connection()

    try:
        jobs_df = pd.read_sql_query("SELECT * FROM jobs ORDER BY started_at DESC", conn)
        quotes_df = pd.read_sql_query("SELECT quote, author, tags FROM quotes ORDER BY author, quote", conn)
    finally:
        conn.close()

    return jobs_df, quotes_df


def main():
    st.title("Book quotes ETL Dashboard")

    if st.button("Run Pipeline", type="primary"):
        try:
            run_etl_job()
        except Exception as error:
            st.error(f"Pipeline failed: {error}")
        else:
            st.success("Pipeline executed successfully!")

    jobs_df, quotes_df = load_dashboard_data()

    st.subheader("Jobs History")
    st.dataframe(jobs_df, width="stretch")

    if not jobs_df.empty and jobs_df.iloc[0]["status"] == "success":
        st.subheader("Quotes Data")
        st.dataframe(quotes_df, width="stretch")


if __name__ == "__main__":
    main()
