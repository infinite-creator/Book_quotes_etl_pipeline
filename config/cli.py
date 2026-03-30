import argparse
from pathlib import Path

from config.settings import OUTPUT_DIR


def build_parser():
    parser = argparse.ArgumentParser(description="Book Quotes ETL Pipeline")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)

    parser.add_argument("--save-raw", action="store_true")

    parser.add_argument("--skip-csv", action="store_true")
    parser.add_argument("--skip-db", action="store_true")

    return parser


def parse_cli_args(argv=None):
    return build_parser().parse_args(argv)


def arg_parser(argv=None):
    return parse_cli_args(argv)