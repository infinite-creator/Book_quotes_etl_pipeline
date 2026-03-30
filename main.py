from config.cli import parse_cli_args
from pipeline.orchestrator import run_pipeline


if __name__ == "__main__":
    run_pipeline(**vars(parse_cli_args()))