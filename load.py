import logging

import pandas as pd 
import sqlite3

def load_to_csv(quotes: list[dict], filename: str = "quotes.csv") -> None:
    df = pd.DataFrame(quotes)
    df.to_csv(filename, index=False)

def load_to_sqlite(quotes: list[dict], db_path: str):
    df = pd.DataFrame(quotes)
       
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTAGER PRIMARY KEY AUTOINCREMENT,
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
