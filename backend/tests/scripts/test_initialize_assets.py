#tests/scripts/test_initialize_assets.py
import subprocess
import json
import os
from sqlalchemy.orm import Session

from src.domain.helpers.path import get_project_root
from src.infrastructure.database.models import Asset
from src.settings import logger


def run_script_with_args(args: list[str]):
    # スクリプトを指定された引数で実行
    result = subprocess.run(["python", "scripts/initialize_assets.py"] + args, capture_output=True, text=True)
    return result

def test_add_asset_success(db_session: Session):
    args = ["--add", "TestAsset"]
    result = run_script_with_args(args)
    assert "資産 'TestAsset' が追加されました。" in result.stdout
    # データベースにアセットが追加されたことを検証
    asset = db_session.query(Asset).filter_by(name="TestAsset").first()
    assert asset is not None

def test_remove_asset_success(db_session: Session):
    # 事前にアセットを追加
    try:
        with db_session.begin():
            db_session.add(Asset(name="TestAssetToRemove"))
    except Exception as e:
        db_session.rollback()
        raise e

    args = ["--remove", "TestAssetToRemove"]
    result = run_script_with_args(args)
    assert "資産 'TestAssetToRemove' が削除されました。" in result.stdout
    # データベースからアセットが削除されたことを検証
    asset = db_session.query(Asset).filter_by(name="TestAssetToRemove").first()
    assert asset is None

def test_initialize_assets_from_config(db_session: Session):
    project_root = get_project_root()
    config_path = os.path.join(project_root, "tests", "scripts", "test_config.json")
    # テスト用設定ファイルを作成
    config_data = {"TestAsset": {"url": "https://example.com"}}
    with open(config_path, "w") as f:
        json.dump(config_data, f)

    args = ["--config", config_path]
    result = run_script_with_args(args)
    assert "資産の初期化が完了しました。" in result.stdout
    # 設定ファイルに基づいてアセットが追加されたことを検証
    asset = db_session.query(Asset).filter_by(name="TestAsset").first()
    assert asset is not None
