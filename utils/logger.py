import logging
from pathlib import Path

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

def get_logger(name: str):

    logger = logging.setLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        #Console handler

        console = logging.StreamHandler()
        console.setFormatter(formatter)

        #File Handler
        file_handler = logging.FileHandler(LOG_DIR / 'app.log')
        file_handler.setFormatter(formatter)

        logger.addHandler(console)
        logger.addHandler(file_handler)
    return logger