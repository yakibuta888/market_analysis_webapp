# tests/application/web/api/test_trade_date_router.py
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from datetime import date
import pytest

from src.application.web.api.dependencies import get_trade_date_service
from src.main import app  # Your FastAPI application instance
from src.domain.entities.trade_date_entity import TradeDateEntity
from src.domain.exceptions.invalid_input_error import InvalidInputError
from src.domain.exceptions.repository_error import RepositoryError
from src.domain.services.trade_date_service import TradeDateService

client = TestClient(app)

# Fixture to mock TradeDateService
@pytest.fixture
def trade_date_service_mock():
    service_mock = MagicMock(spec=TradeDateService)
    return service_mock

@pytest.fixture
def get_trade_date_service_mock(trade_date_service_mock: MagicMock):
    # get_trade_date_service が返すべき関数をモックする
    def _mock_dependency(graph_type: str):
        return trade_date_service_mock
    return _mock_dependency

@pytest.fixture(autouse=True)
def override_get_trade_date_service(get_trade_date_service_mock: MagicMock):
    # get_trade_date_service 依存関係をモックに置き換える
    app.dependency_overrides[get_trade_date_service] = lambda: get_trade_date_service_mock
    yield
    app.dependency_overrides.clear()


def test_get_trade_dates_success(trade_date_service_mock: MagicMock):
    # Set up mock return values
    mock_date_entity = TradeDateEntity(date(2023, 1, 1))
    trade_date_service_mock.fetch_trade_dates.return_value = [mock_date_entity]

    response = client.get("/trade-dates/?graph_type=futures&asset_name=Gold&start_date=2023-01-01&end_date=2023-01-01&skip=0&limit=10")

    assert response.status_code == 200
    assert response.json() == {"trade_dates": ["2023-01-01"]}
    trade_date_service_mock.fetch_trade_dates.assert_called_once_with("Gold", date(2023, 1, 1), date(2023, 1, 1), 0, 10)

def test_get_trade_dates_invalid_input(trade_date_service_mock: MagicMock):
    trade_date_service_mock.fetch_trade_dates.side_effect = InvalidInputError("Invalid asset name.")

    response = client.get("/trade-dates/?graph_type=futures&asset_name=&start_date=2023-01-01&end_date=2023-01-01")
    assert response.status_code == 400
    assert "Invalid asset name" in response.json()['detail']

def test_get_trade_dates_data_not_found(trade_date_service_mock: MagicMock):
    trade_date_service_mock.fetch_trade_dates.return_value = []

    response = client.get("/trade-dates/?graph_type=futures&asset_name=Gold&start_date=2023-01-01&end_date=2023-01-01")
    assert response.status_code == 404
    assert "No trade dates found" in response.json()['detail']

def test_get_trade_dates_value_error(trade_date_service_mock: MagicMock):
    # サービスがValueErrorを発生させるように設定
    trade_date_service_mock.fetch_trade_dates.side_effect = ValueError("Invalid date format")

    response = client.get("/trade-dates/?graph_type=futures&asset_name=Gold&start_date=bad-date-format&end_date=2023-01-01")

    assert response.status_code == 422
    assert any("Input should be a valid date or datetime" in error["msg"] for error in response.json()["detail"])   # モジュールのバリデーションが優先されている

def test_get_trade_dates_type_error(trade_date_service_mock: MagicMock):
    # サービスがTypeErrorを発生させるように設定
    trade_date_service_mock.fetch_trade_dates.side_effect = TypeError("Expected string but got integer")

    response = client.get("/trade-dates/?graph_type=futures&asset_name=123&start_date=2023-01-01&end_date=2023-01-01")

    assert response.status_code == 422
    assert "Expected string but got integer" in response.json()["detail"]

def test_get_trade_dates_repository_error(trade_date_service_mock: MagicMock):
    # サービスがRepositoryErrorを発生させるように設定
    trade_date_service_mock.fetch_trade_dates.side_effect = RepositoryError("Database error")

    response = client.get("/trade-dates/?graph_type=futures&asset_name=Gold&start_date=2023-01-01&end_date=2023-01-01")

    assert response.status_code == 500
    assert "Error accessing data repository" in response.json()["detail"]

def test_get_trade_dates_server_error(trade_date_service_mock: MagicMock):
    trade_date_service_mock.fetch_trade_dates.side_effect = Exception("Unexpected error")

    response = client.get("/trade-dates/?graph_type=futures&asset_name=Gold&start_date=2023-01-01&end_date=2023-01-01")
    assert response.status_code == 500
    assert "An unexpected error occurred." in response.json()['detail']
