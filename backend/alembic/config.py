# alembic/config.py

# Alembic設定ファイルの生成用スクリプト
from pathlib import Path

from src.domain.helpers.path import get_project_root
from src.infrastructure.database.database import DATABASE_URL, TEST_DATABASE_URL


def generate_alembic_config(testing: bool=False) -> None:
    project_root = get_project_root()

    alembic_ini_path = project_root / 'alembic.ini'
    alembic_ini_tpl_path = project_root / 'alembic.ini.tpl'

    template_path = alembic_ini_tpl_path
    output_path = alembic_ini_path
    db_url = TEST_DATABASE_URL if testing else DATABASE_URL
    with open(template_path, 'r') as file:
        config = file.read()
    config = config.replace('${DATABASE_URL}', db_url)
    with open(output_path, 'w') as file:
        file.write(config)
