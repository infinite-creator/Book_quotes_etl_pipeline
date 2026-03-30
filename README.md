# Quotes ETL Pipeline

This project is a small ETL pipeline built in Python.

## What it does

- Extract quotes, authors, and tags from quotes.toscrape.com
- Transform and clean data
- Remove duplicate quotes
- Loads the final data into CSV and SQLite

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the ETL pipeline:

```bash
python main.py
python main.py --save-raw
python main.py --output-dir custom-output
python main.py --skip-csv
python main.py --skip-db
```

Run the Streamlit dashboard:

```bash
streamlit run app/main.py
```

## Tech Stack

- Python
- BeautifulSoup
- requests
- pandas
- SQLite
