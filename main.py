from pathlib import Path

from app.pipeline.extract import extract_all_quotes
from app.pipeline.transform import transform_quotes
from app.pipeline.load import load_to_csv, load_to_sqlite, load_raw_data_to_json

from app.config.settings import CSV_FILE, SQLITE_DB, RAW_JSON_FILE
from app.config.logger_config import log_run_indicator, set_logger
from app.config.cli import arg_parser

from app.models.paths import OutputPaths

def main():
    args = arg_parser()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    paths = OutputPaths(
        json = output_dir / RAW_JSON_FILE,
        csv = output_dir / CSV_FILE,
        db = output_dir / SQLITE_DB
    )

    set_logger()
    log_run_indicator("START")
    
    raw_quotes = extract_all_quotes()
    
    #if --save-raw arg passed, load raw data to json
    if args.save_raw:
        load_raw_data_to_json(raw_quotes, paths.json)
    

    transformed_quotes = transform_quotes(raw_quotes)

    #Loading to CSV if step is not skipped 
    if not args.skip_csv:
        load_to_csv(transformed_quotes, paths.csv)
    
    #Writing to db if step is not skipped
    if not args.skip_db:
        load_to_sqlite(transformed_quotes, paths.db)
    
    log_run_indicator("END")
    
if(__name__ == "__main__"):
    main()
