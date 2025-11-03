import logging
from datetime import datetime
import os

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
    return logging.getLogger("GokuAI")
