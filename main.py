from pathlib import Path
from extract import extract_all_quotes
from transform import transform_quotes
from load import load_to_csv, load_to_sqlite
import logging 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    logging.info("Starting ETL pipeline...")
    
    raw_quotes = extract_all_quotes()
    logging.info(f"Extracted {len(raw_quotes)} quotes.")
    
    with open(output_dir / "raw_quotes.json", "w", encoding="utf-8") as f:
        import json
        json.dump(raw_quotes, f, ensure_ascii=False, indent=2)
    logging.info("Raw quotes saved to JSON.")
    
    transformed_quotes = transform_quotes(raw_quotes)
    logging.info(f"Transformed {len(transformed_quotes)} unique quotes.")
    
    load_to_csv(transformed_quotes, output_dir/"quotes.csv")
    logging.info("Quotes loaded to CSV.")
    
    load_to_sqlite(transformed_quotes, output_dir/"quotes.db")
    logging.info("Quotes loaded to SQLite database.")
    
    logging.info("ETL pipeline completed successfully.")
    
if(__name__ == "__main__"):
    main()
