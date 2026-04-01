from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BASE_URL = "https://quotes.toscrape.com/page/{}/"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = "etl_pipeline.log"
LOG_PATH = LOG_DIR / LOG_FILE
CSV_FILE = "quotes.csv"
SQLITE_DB = PROJECT_ROOT / "db" / "database.db"
RAW_JSON_FILE = "raw_quotes.json"
