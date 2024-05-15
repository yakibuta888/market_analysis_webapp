# tests/application/web/api/test_futures_data_router.py
import pandas as pd
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from src.application.web.api.dependencies import get_futures_data_service
from src.main import app  # FastAPIアプリケーションのインスタンス
from src.domain.services.futures_data_service import FuturesDataService


# FastAPIアプリケーションのTestClientを作成
client = TestClient(app, raise_server_exceptions=False)

# モックを使用するためのフィクスチャ
@pytest.fixture
def futures_data_service_mock(monkeypatch: pytest.MonkeyPatch):
    service_mock = MagicMock(spec=FuturesDataService)
    monkeypatch.setattr("src.application.web.api.dependencies.get_futures_data_service", lambda: service_mock)
    return service_mock

# モック用のテストデータ
test_data = pd.DataFrame({
    "trade_date": [datetime(2023, 1, 1).date(), datetime(2023, 1, 2).date()],
    "month": [datetime(2023, 2, 1), datetime(2023, 3, 1)],
    "settle": [1500, 1600],
    "volume": [100, 200],
    "open_interest": [10, 20]
})

# モック用のレスポンスデータ
expected_response_data = {
    "data": [
        {
            "trade_date": "2023-01-01",
            "month": "2023-02",
            "settle": 1500,
            "volume": 100,
            "open_interest": 10
        },
        {
            "trade_date": "2023-01-02",
            "month": "2023-03",
            "settle": 1600,
            "volume": 200,
            "open_interest": 20
        }
    ]
}


def test_get_futures_data_success(futures_data_service_mock: MagicMock):
    app.dependency_overrides[get_futures_data_service] = lambda: futures_data_service_mock
    futures_data_service_mock.make_dataframe.return_value = test_data
    futures_data_service_mock.add_settlement_spread.return_value = test_data

    # APIエンドポイントのテスト実行
    response = client.get("/futures-data/gold?trade_dates=2023-01-01&trade_dates=2023-01-02")
    app.dependency_overrides.clear()

    # レスポンスの検証
    assert response.status_code == 200
    assert response.json() == expected_response_data

    # モックが呼び出されたことを確認
    futures_data_service_mock.make_dataframe.assert_called_once_with('gold', [datetime(2023, 1, 1).date(), datetime(2023, 1, 2).date()])
    futures_data_service_mock.add_settlement_spread.assert_called_once()


def test_get_futures_data_invalid_input_date_format():
    # 日付の形式が不正な場合のテスト
    response = client.get("/futures-data/gold?trade_dates=invalid-date-format")

    # レスポンスの検証
    assert response.status_code == 422  # 422 Unprocessable Entityが適切なステータスコード
    assert "detail" in response.json()
    assert any("Input should be a valid date or datetime" in error["msg"] for error in response.json()["detail"])


def test_get_futures_data_missing_asset_name():
    # 資産名が空の場合のテスト
    response = client.get("/futures-data/?trade_dates=2023-01-01")

    # レスポンスの検証
    assert response.status_code == 404  # 資産名がURLパスに含まれていないため、404 Not Foundが適切


def test_get_futures_data_no_data_found(futures_data_service_mock: MagicMock):
    # データが見つからない場合のテスト
    futures_data_service_mock.make_dataframe.return_value = pd.DataFrame()

    # APIエンドポイントのテスト実行
    response = client.get("/futures-data/gold?trade_dates=2023-01-01")

    # レスポンスの検証
    assert response.status_code == 404  # 404 Not Foundが適切
    assert "detail" in response.json()
    assert "No data found for the given parameters." in response.json().get("detail")


def test_get_futures_data_future_trade_date():
    # 未来の取引日を指定した場合のテスト
    future_date = "9999-12-31"
    response = client.get(f"/futures-data/gold?trade_dates={future_date}")

    # レスポンスの検証
    assert response.status_code == 422  # pydanticのバリデーションエラーが422 Unprocessable Entityを返す
    assert "detail" in response.json()
    assert "取引日は過去または今日でなければなりません。" in response.json().get("detail")


def test_get_futures_data_server_error(futures_data_service_mock: MagicMock):
    app.dependency_overrides[get_futures_data_service] = lambda: futures_data_service_mock
    futures_data_service_mock.make_dataframe.return_value = test_data
    # 内部サーバーエラーをシミュレートするために、エラーを発生させる
    futures_data_service_mock.make_dataframe.side_effect = Exception("Unexpected error")

    # エンドポイントへのリクエストを実行
    response = client.get("/futures-data/gold?trade_dates=2023-01-01")
    app.dependency_overrides.clear()

    # レスポンスの検証
    assert response.status_code == 500
    assert "detail" in response.json()
