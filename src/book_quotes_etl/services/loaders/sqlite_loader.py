import pandas as pd 

def load_to_sqlite(quotes: list[dict], conn):
    df = pd.DataFrame(quotes)
       
    cursor = conn.cursor()
    
    cursor.executemany("""
        INSERT OR IGNORE INTO quotes (quote, author, tags) VALUES (?, ?, ?)
    """, df[["quote", "author", "tags"]].values.tolist())
    
    conn.commit()
