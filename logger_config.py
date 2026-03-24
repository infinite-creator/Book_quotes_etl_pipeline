from datetime import datetime
import logging
from pathlib import Path

from config import LOG_DIR, LOG_FILE

def set_logger() -> None:
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s', 
        handlers=[
            logging.FileHandler(rf"{LOG_DIR}/{LOG_FILE}", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
def log_run_indicator(stage: str) -> None:
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    separator = ("\n" + "-"*120 + "\n" + f"{stage} PIPELINE AT {run_time}" + "\n" + "-"*120 +"\n")
    
    with open(rf"{LOG_DIR}/{LOG_FILE}", "a", encoding="utf-8") as log_file:
        log_file.write(separator)
