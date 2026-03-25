import argparse

from config.settings import OUTPUT_DIR

def arg_parser():
    parser = argparse.ArgumentParser("Book Quotes ETL Pipeline")
    parser.add_argument("--output-dir", default=OUTPUT_DIR)

    parser.add_argument("--save-raw", action="store_true")

    parser.add_argument("--skip-csv", action="store_true")
    parser.add_argument("--skip-db", action="store_true")

    return parser.parse_args()