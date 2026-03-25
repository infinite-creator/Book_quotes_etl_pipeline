# Quotes ETL Pipeline

This project is a small ETL pipeline built in Python

## What it does

- Extract quotes, authors, and tags from quotes.toscrape.com
- Transforms and clean data
- Remove dupliocate quotes
- Loads the final data into CSV and SQLite

## Usage 
Run full pipeline: ``python main.py``
Run with raw data saved: ``python main.py --save-raw``
Custom output directory("output" by default): ``python main.py --output-dir <name>``
Skip CSV file creation: ``python main.py --skip-csv``
Skip writing into SQLite DB file: ``python main.py --skip-db``


## Tech Stack

- Python
- BeautifulSoup
- requests
- pandas
- sqlite

