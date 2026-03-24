from pathlib import Path
from config import CSV_FILE, OUTPUT_DIR, RAW_JSON_FILE, SQLITE_DB
from extract import extract_all_quotes
from logger_config import log_run_indicator, set_logger
from transform import transform_quotes
from load import load_to_csv, load_to_sqlite
import logging 

def main():
    set_logger()
    log_run_indicator("START")
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    
    logging.info("Starting ETL pipeline...")
    
    raw_quotes = extract_all_quotes()
    logging.info(f"Extracted {len(raw_quotes)} quotes.")
    
    with open(RAW_JSON_FILE, "w", encoding="utf-8") as f:
        import json
        json.dump(raw_quotes, f, ensure_ascii=False, indent=2)
    logging.info("Raw quotes saved to JSON.")
    
    transformed_quotes = transform_quotes(raw_quotes)
    logging.info(f"Transformed {len(transformed_quotes)} unique quotes.")
    
    load_to_csv(transformed_quotes, CSV_FILE)
    logging.info("Quotes loaded to CSV.")
    
    load_to_sqlite(transformed_quotes, SQLITE_DB)
    logging.info("Quotes loaded to SQLite database.")
    
    logging.info("ETL pipeline completed successfully.")
    log_run_indicator("END")
    
if(__name__ == "__main__"):
    main()
