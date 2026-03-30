from pathlib import Path
import logging

from db.database import get_connection
from pipeline.extract import extract_all_quotes
from pipeline.transform import transform_quotes

from services.loaders.sqlite_loader import load_to_sqlite
from services.loaders.csv_loader import load_to_csv
from services.loaders.json_loader import load_raw_data_to_json

from config.settings import CSV_FILE, OUTPUT_DIR, RAW_JSON_FILE
from config.logger_config import log_run_indicator, set_logger
from config.cli import parse_cli_args

from models.paths import OutputPaths


def run_pipeline(*, conn=None, output_dir=OUTPUT_DIR, save_raw=False, skip_csv=False, skip_db=False):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = OutputPaths(
        json = output_dir / RAW_JSON_FILE,
        csv = output_dir / CSV_FILE,
    )

    set_logger()
    log_run_indicator("START")
    
    raw_quotes = extract_all_quotes()
    
    if save_raw:
        load_raw_data_to_json(raw_quotes, paths.json)
        logging.info("Raw quotes saved to JSON.")
    

    transformed_quotes = transform_quotes(raw_quotes)

    if not skip_csv:
        load_to_csv(transformed_quotes, paths.csv)
        logging.info("Quotes loaded to CSV.")

    active_conn = conn
    owns_connection = False

    try:
        if not skip_db:
            if active_conn is None:
                active_conn = get_connection()
                owns_connection = True

            load_to_sqlite(transformed_quotes, active_conn)
            logging.info("Quotes loaded to SQLite database.")
    finally:
        log_run_indicator("END")

        if owns_connection and active_conn is not None:
            active_conn.close()
    
if(__name__ == "__main__"):
    run_pipeline(**vars(parse_cli_args()))
