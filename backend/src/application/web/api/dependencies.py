# src/application/web/api/dependencies.py
import os

from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator, Callable
from typing import Any

from src.settings import logger
from src.domain.services.asset_service import AssetService
from src.domain.services.futures_data_service import FuturesDataService
from src.domain.services.trade_date_service import TradeDateService
from src.domain.services.user_service import UserService
from src.domain.repositories.asset_repository import AssetRepository
from src.domain.repositories.futures_data_repository import FuturesDataRepository
from src.domain.repositories.trade_date_repository import TradeDateRepository
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.mysql.asset_repository_mysql import AssetRepositoryMysql
from src.infrastructure.mysql.futures_data_repository_mysql import FuturesDataRepositoryMysql
from src.infrastructure.mysql.futures_data_trade_date_repository_mysql import FuturesDataTradeDateRepositoryMysql
from src.infrastructure.mysql.user_repository_mysql import UserRepositoryMysql
from src.infrastructure.database.database import db_session


def get_db() -> Generator[Session, Any, Any]:
    db = db_session()
    try:
        yield db
    finally:
        db.close()

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    logger.info("Fetching UserRepositoryMysql")
    return UserRepositoryMysql(db)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repository = get_user_repository(db)
    return UserService(user_repository)

def get_futures_data_repository(db: Session = Depends(get_db)) -> FuturesDataRepository:
    logger.info("Fetching FuturesDataRepositoryMysql")
    return FuturesDataRepositoryMysql(db)

def get_futures_data_service(db: Session = Depends(get_db)) -> FuturesDataService:
    futures_data_repository = get_futures_data_repository(db)
    return FuturesDataService(futures_data_repository)

def get_asset_repository(db: Session = Depends(get_db)) -> AssetRepository:
    logger.info("Fetching AssetRepositoryMysql")
    return AssetRepositoryMysql(db)

def get_asset_service(db: Session = Depends(get_db)) -> AssetService:
    asset_repository = get_asset_repository(db)
    return AssetService(asset_repository)

def get_trade_date_repository(graph_type: str, db: Session = Depends(get_db)) -> TradeDateRepository:
    if graph_type == "futures-data":
        logger.info("Fetching FuturesDataTradeDateRepositoryMysql")
        return FuturesDataTradeDateRepositoryMysql(db)
    else:
        logger.error(f"Unsupported graph type: {graph_type}")
        raise ValueError("Unsupported graph type")

def get_trade_date_service(db: Session = Depends(get_db)) -> Callable[[str], TradeDateService]:
    def _dependency(graph_type: str):
        trade_date_repository = get_trade_date_repository(graph_type, db)
        return TradeDateService(trade_date_repository)
    return _dependency
