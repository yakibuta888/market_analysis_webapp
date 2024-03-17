# scripts/initialize_assets.py

import argparse
from sqlalchemy.orm import Session
from typing import Generator, Any

from src.domain.services.asset_service import AssetService
from src.infrastructure.database.database import db_session
from src.infrastructure.mysql.asset_repository_mysql import AssetRepositoryMysql



def get_db() -> Generator[Session, Any, Any]:
    db = db_session()
    try:
        yield db
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description="アセット管理スクリプト")
    parser.add_argument("--config", type=str, help="設定ファイルのパス")
    parser.add_argument("--add", type=str, help="追加するアセット名")
    parser.add_argument("--remove", type=str, help="削除するアセット名")

    args = parser.parse_args()

    asset_repository = AssetRepositoryMysql(next(get_db()))
    asset_service = AssetService(asset_repository)

    if args.config:
        asset_service.initialize_assets_from_config(args.config)
        print("資産の初期化が完了しました。")
    elif args.add:
        asset_service.add_asset(args.add)
        print(f"資産 '{args.add}' が追加されました。")
    elif args.remove:
        asset_service.remove_asset(args.remove)
        print(f"資産 '{args.remove}' が削除されました。")
    else:
        print("操作を指定してください。--add, --remove, または --config のいずれかの引数を使用します。")

if __name__ == "__main__":
    main()
