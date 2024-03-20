import json
import pytest
from unittest.mock import Mock, patch

from src.domain.services.asset_service import AssetService
from src.domain.entities.asset_entity import AssetEntity
from src.domain.repositories.asset_repository import AssetRepository
from src.domain.value_objects.name import Name
from src.infrastructure.database.models import Asset as AssetModel


@pytest.fixture
def mock_asset_repository():
    """AssetRepositoryのモックを生成するフィクスチャ"""
    return Mock(spec=AssetRepository)

@pytest.fixture
def asset_service(mock_asset_repository: Mock) -> AssetService:
    """AssetServiceのインスタンスを生成するフィクスチャ、依存関係はモックを使用"""
    return AssetService(mock_asset_repository)


def test_add_asset_success(asset_service: AssetService, mock_asset_repository: Mock):
    """add_assetメソッドが成功するケースをテスト"""
    asset_name = "Test Asset"
    # モックの振る舞いを設定
    mock_asset_repository.create.return_value = AssetModel(id=1, name=asset_name)

    # テスト実行
    asset_service.add_asset(asset_name)

    # モックの呼び出しを検証
    mock_asset_repository.create.assert_called_once()


def test_add_asset_with_invalid_name_raises_error(asset_service: AssetService):
    """無効な名前を渡したときにエラーが発生することをテスト"""
    invalid_name = ""  # 無効な名前（空文字）を設定
    # モックの振る舞いを設定（このケースでは、モックは直接使用しないが、必要に応じて設定可能）

    with pytest.raises(ValueError) as excinfo:
        asset_service.add_asset(invalid_name)

    # 発生した例外のメッセージを検証
    assert "名前は空にできません。" in str(excinfo.value)


def test_remove_asset_success(asset_service: AssetService, mock_asset_repository: Mock):
    """remove_assetメソッドが成功するケースをテスト"""
    asset_name = "Test Asset"
    # モックの振る舞いを設定
    mock_asset_repository.exists_by_name.return_value = True

    # テスト実行
    asset_service.remove_asset(asset_name)

    # モックの呼び出しを検証
    mock_asset_repository.delete.assert_called_once_with(Name(asset_name))


def test_remove_asset_nonexistent_with_warning(asset_service: AssetService, mock_asset_repository: Mock):
    nonexistent_asset_name = "Nonexistent Asset"
    mock_asset_repository.exists_by_name.return_value = False

    # logger の warning メソッドの呼び出しをパッチします。
    with patch('src.domain.services.asset_service.logger') as mock_logger:
        # 存在しないアセットを削除しようとするテストを実行します。
        asset_service.remove_asset(nonexistent_asset_name)

        # アセットが存在しない場合に適切な警告ログが出力されることを検証します。
        mock_logger.warning.assert_called_once_with(f"資産 '{nonexistent_asset_name}' が見つかりません。")


def test_initialize_assets_from_config(tmpdir: str, asset_service: AssetService, mock_asset_repository: Mock):
    # テスト用の設定ファイルを作成
    config_path = tmpdir.join("config.json")
    config_data = {
        "Gold": {
            "settlements": "https://example.com/gold/settlements",
            "volume_and_open_interest": "https://example.com/gold/volume"
        },
        "Silver": {
            "settlements": "https://example.com/silver/settlements",
            "volume_and_open_interest": "https://example.com/silver/volume"
        }
    }
    with open(config_path, "w") as f:
        json.dump(config_data, f)

    mock_asset_repository.exists_by_name.side_effect = [False, False, True, True]  # 1回目は存在しない、2回目は存在するとする

    # initialize_assets_from_config メソッドをテスト
    asset_service.initialize_assets_from_config(str(config_path))

    # 資産が追加されたことを検証
    expected_calls = [ # type: ignore
        ((AssetEntity.new_entity(Name("Gold")),), {}),
        ((AssetEntity.new_entity(Name("Silver")),), {})
    ]
    assert mock_asset_repository.create.call_count == len(config_data)
    mock_asset_repository.create.assert_has_calls(expected_calls, any_order=True)


def test_fetch_asset_id(asset_service: AssetService, mock_asset_repository: Mock):
    # 準備：想定される戻り値の設定
    mock_asset = AssetModel(id=1, name="Test Asset")
    mock_asset_repository.fetch_by_name.return_value = mock_asset

    # 実行：fetch_asset_idメソッドをテスト
    asset_id = asset_service.fetch_asset_id("Test Asset")

    # 検証：fetch_by_nameメソッドが期待通りの引数で呼び出され、期待する戻り値を返すこと
    mock_asset_repository.fetch_by_name.assert_called_once_with(Name("Test Asset"))
    assert asset_id == 1
