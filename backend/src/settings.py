# src/settings.py

import logging.config
import os
import yaml
from pathlib import Path


CWD: Path = Path(__file__).resolve().parent
LOG_CONFIG_PATH: str = os.path.normpath(os.path.join(CWD, "log/log_config.yaml"))


def setup_logging() -> None:
    with open(LOG_CONFIG_PATH, encoding='utf-8') as f:
        log_config = yaml.safe_load(f)
    logging.config.dictConfig(log_config)  # type: ignore


setup_logging()
logger = logging.getLogger(__name__)
