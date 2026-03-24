from extract import extract_all_quotes
from transform import transform_quotes
from load import load_to_csv, load_to_sqlite

def main():
    print("Starting ETL pipeline...")
    
    raw_quotes = extract_all_quotes()
    print(f"Extracted {len(raw_quotes)} quotes.")
    
    transformed_quotes = transform_quotes(raw_quotes)
    print(f"Transformed {len(transformed_quotes)} unique quotes.")
    
    load_to_csv(transformed_quotes)
    print("Quotes loaded to CSV.")
    
    load_to_sqlite(transformed_quotes, "quotes.db")
    print("Quotes loaded to SQLite database.")
    
    print("ETL pipeline completed successfully.")
    
if(__name__ == "__main__"):
    main()
