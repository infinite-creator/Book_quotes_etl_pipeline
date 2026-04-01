from book_quotes_etl.config.cli import parse_cli_args
from book_quotes_etl.pipeline.orchestrator import run_pipeline


if __name__ == "__main__":
    run_pipeline(**vars(parse_cli_args()))