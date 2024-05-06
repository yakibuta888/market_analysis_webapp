# tests/application/web/api/test_asset_router.py
import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from src.application.web.api.dependencies import get_asset_service
from src.domain.entities.asset_entity import AssetEntity
from src.domain.exceptions.asset_not_found_error import AssetNotFoundError
from src.domain.value_objects.name import Name
from src.main import app
from src.domain.services.asset_service import AssetService


# FastAPIアプリケーションのTestClientを作成
client = TestClient(app, raise_server_exceptions=False)

# モックを使用するためのフィクスチャ
@pytest.fixture
def asset_service_mock(monkeypatch: pytest.MonkeyPatch):
    service_mock = MagicMock(spec=AssetService)
    monkeypatch.setattr("src.application.web.api.dependencies.get_asset_service", lambda: service_mock)
    return service_mock

# モック用のテストデータ
test_data = [
    AssetEntity(id=1, name=Name("gold")),
    AssetEntity(id=2, name=Name("silver")),
    AssetEntity(id=3, name=Name("crude_oil")),
]

# モック用のレスポンスデータ
expected_response_data = [
    {"id": 1, "name": "gold"},
    {"id": 2, "name": "silver"},
    {"id": 3, "name": "crude_oil"}
]


def test_fetch_assets_success(asset_service_mock: MagicMock):
    app.dependency_overrides[get_asset_service] = lambda: asset_service_mock
    asset_service_mock.fetch_all.return_value = test_data

    # APIエンドポイントのテスト実行
    response = client.get("/assets")
    app.dependency_overrides.clear()

    # レスポンスの検証
    assert response.status_code == 200
    assert response.json() == expected_response_data

    # モックが呼び出されたことを確認
    asset_service_mock.fetch_all.assert_called_once()


def test_fetch_assets_not_found(asset_service_mock: MagicMock):
    app.dependency_overrides[get_asset_service] = lambda: asset_service_mock
    asset_service_mock.fetch_all.side_effect = AssetNotFoundError("No assets found")

    # APIエンドポイントのテスト実行
    response = client.get("/assets")
    app.dependency_overrides.clear()

    # レスポンスの検証
    assert response.status_code == 404
    response_data = json.loads(response.json()['detail'])
    assert response_data['error_type'] == 'AssetNotFound'
    assert response_data['message'] == 'Asset not found'
    assert response_data['detail'] == 'No assets found'
    asset_service_mock.fetch_all.assert_called_once()


def test_fetch_assets_server_error(asset_service_mock: MagicMock):
    app.dependency_overrides[get_asset_service] = lambda: asset_service_mock
    asset_service_mock.fetch_all.side_effect = Exception("Unexpected error")

    # APIエンドポイントのテスト実行
    response = client.get("/assets")
    app.dependency_overrides.clear()

    # レスポンスの検証
    assert response.status_code == 500
    response_data = json.loads(response.json()['detail'])
    assert response_data['error_type'] == 'InternalServerError'
    assert response_data['message'] == 'Internal server error'
    assert response_data['detail'] == 'Unexpected error'
    asset_service_mock.fetch_all.assert_called_once()
