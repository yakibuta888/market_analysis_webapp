# tests/infrastructure/test_asset_repository.py
import pytest
from sqlalchemy.orm import Session

from src.infrastructure.repositories.asset_repository_mysql import AssetRepositoryMysql
from src.infrastructure.database.models import Asset
from src.domain.entities.asset_entity import AssetEntity
from src.domain.value_objects.name import Name

def test_add_asset_success(test_session: Session):
    asset_repository = AssetRepositoryMysql(session=test_session)
    asset_name = "Test Asset"
    asset_entity = AssetEntity.new_entity(name=Name(asset_name))

    # アセットを追加
    asset_repository.create(asset_entity)

    # データベースにアセットが追加されたか確認
    added_asset = test_session.query(Asset).filter(Asset.name == asset_name).first()
    assert added_asset is not None
    assert added_asset.name == asset_name

def test_remove_asset_success(test_session: Session):
    asset_repository = AssetRepositoryMysql(session=test_session)
    asset_name = "Test Asset"
    asset_entity = AssetEntity.new_entity(name=Name(asset_name))

    # 事前にアセットを追加
    asset_repository.create(asset_entity)

    # アセットを削除
    asset_repository.delete(asset_entity.name)

    # データベースからアセットが削除されたか確認
    removed_asset = test_session.query(Asset).filter(Asset.name == asset_name).first()
    assert removed_asset is None

def test_fetch_by_name_success(test_session: Session):
    # AssetRepositoryMysqlのインスタンスを作成
    asset_repository = AssetRepositoryMysql(session=test_session)
    asset_name = "Test Asset"
    asset_entity = AssetEntity.new_entity(name=Name(asset_name))

    # 事前にアセットをデータベースに追加
    asset_repository.create(asset_entity)

    # fetch_by_nameメソッドを使用してアセットを取得
    fetched_asset = asset_repository.fetch_by_name(Name(asset_name))

    # 取得したアセットが正しいか確認
    assert fetched_asset is not None
    assert fetched_asset.name == asset_name

def test_fetch_by_name_nonexistent(test_session: Session):
    # AssetRepositoryMysqlのインスタンスを作成
    asset_repository = AssetRepositoryMysql(session=test_session)
    nonexistent_asset_name = "Nonexistent Asset"

    # 存在しないアセット名でfetch_by_nameメソッドを呼び出し、例外が発生することを確認
    with pytest.raises(Exception) as excinfo:
        asset_repository.fetch_by_name(Name(nonexistent_asset_name))

    assert "Asset with name" in str(excinfo.value)

def test_exists_by_name_true(test_session: Session):
    # AssetRepositoryMysqlのインスタンスを作成
    asset_repository = AssetRepositoryMysql(session=test_session)
    asset_name = "Test Asset"
    asset_entity = AssetEntity.new_entity(name=Name(asset_name))

    # 事前にアセットをデータベースに追加
    asset_repository.create(asset_entity)

    # exists_by_nameメソッドを使用してアセットの存在を確認
    exists = asset_repository.exists_by_name(Name(asset_name))

    assert exists is True

def test_exists_by_name_false(test_session: Session):
    # AssetRepositoryMysqlのインスタンスを作成
    asset_repository = AssetRepositoryMysql(session=test_session)
    nonexistent_asset_name = "Nonexistent Asset"

    # 存在しないアセット名でexists_by_nameメソッドを呼び出し、アセットが存在しないことを確認
    exists = asset_repository.exists_by_name(Name(nonexistent_asset_name))

    assert exists is False
