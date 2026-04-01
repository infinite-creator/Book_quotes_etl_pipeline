from datetime import datetime
import logging

from book_quotes_etl.config.settings import LOG_DIR, LOG_PATH

def set_logger() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s', 
        handlers=[
            logging.FileHandler(LOG_PATH, encoding='utf-8'),
            logging.StreamHandler()
        ],
        force=True,
    )
    
def log_run_indicator(stage: str) -> None:
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    separator = ("\n" + "-"*120 + "\n" + f"{stage} PIPELINE AT {run_time}" + "\n" + "-"*120 +"\n")
    
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    with open(LOG_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(separator)
