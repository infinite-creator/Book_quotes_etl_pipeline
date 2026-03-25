import logging
import json

import pandas as pd 
import sqlite3

#Load raw data to JSON
def load_raw_data_to_json(raw_quotes, json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(raw_quotes, f, ensure_ascii=False, indent=2)

    logging.info("Raw quotes saved to JSON.")

#Load transdormed data to CSV
def load_to_csv(quotes: list[dict], csv_path):
    df = pd.DataFrame(quotes)
    df.to_csv(csv_path, index=False)
    
    logging.info("Quotes loaded to SQLite database.")

#Load transdormed data to DB SQLite
def load_to_sqlite(quotes: list[dict], db_path):
    df = pd.DataFrame(quotes)
       
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            author TEXT NOT NULL,
            tags TEXT,
            UNIQUE(quote, author)
        )
    """)
    
    cursor.executemany("""
        INSERT OR IGNORE INTO quotes (quote, author, tags) VALUES (?, ?, ?)
    """, df[["quote", "author", "tags"]].values.tolist())
    
    conn.commit()
    conn.close()

    logging.info("Quotes loaded to CSV.")
