import logging.config
import os
import yaml
from pathlib import Path


cwd: Path = Path(__file__).resolve().parent
log_config_path: str = os.path.normpath(os.path.join(cwd, "log/log_config.yaml"))

with open(log_config_path, encoding='utf-8') as f:
    log_config = yaml.safe_load(f)
logging.config.dictConfig(log_config)  # type: ignore
logger = logging.getLogger(__name__)
