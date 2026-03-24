import pandas as pd 
import sqlite3

def load_to_csv(quotes: list[dict], filename: str = "quotes.csv") -> None:
    df = pd.DataFrame(quotes)
    df.to_csv(filename, index=False)

def load_to_sqlite(quotes: list[dict], db_path: str):
    df = pd.DataFrame(quotes)
       
    conn = sqlite3.connect(db_path)
    df.to_sql("quotes", conn, if_exists="replace", index=False)
    conn.close()
