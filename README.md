# Quotes ETL Pipeline

This project is a small ETL pipeline built in Python.

## What it does

- Extract quotes, authors, and tags from quotes.toscrape.com
- Transform and clean data
- Remove duplicate quotes
- Loads the final data into CSV and SQLite

## Project Structure

```
src/book_quotes_etl/          # Main package
  config/                      # Configuration and CLI
  db/                          # Database models and connection
  pipeline/                    # Extract, transform, orchestration
  models/                      # Data structures
  services/                    # Job management and loaders
tests/                         # Test suite
app/                          # Streamlit dashboard
```

## Setup

Install the package in development (editable) mode:

```bash
pip install -e .
```

Or install with dev dependencies (including pytest):

```bash
pip install -e ".[dev]"
```

## Usage

### CLI: Run the ETL pipeline

```bash
python main.py
python main.py --save-raw
python main.py --output-dir custom-output
python main.py --skip-csv
python main.py --skip-db
```

### Dashboard: Run the Streamlit dashboard

```bash
streamlit run app/main.py
```

### Testing

Run the full test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src/book_quotes_etl --cov-report=html
```

Run specific test file:

```bash
pytest tests/test_transform.py   # Transform logic tests
pytest tests/test_schema.py      # Schema bootstrap tests
pytest tests/test_pipeline.py    # Pipeline smoke tests
```

## Tech Stack

- Python
- BeautifulSoup
- requests
- pandas
- SQLite
- Streamlit (dashboard)
- pytest (testing)

