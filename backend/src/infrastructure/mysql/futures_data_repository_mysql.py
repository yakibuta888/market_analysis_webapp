# src/infrastracture/repositories/futures_data_repository_mysql.py
from datetime import date
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain.entities.futures_data_entity import FuturesDataEntity
from src.domain.repositories.futures_data_repository import FuturesDataRepository


class FuturesDataRepositoryMysql(FuturesDataRepository):
    def __init__(self, session: Session):
        self.session = session

    def fetch_by_asset_and_date(self, asset_name: str, trade_date: date) -> list[FuturesDataEntity]:
        result = self.session.execute(
            text("""
            SELECT
                a.id AS asset_id,
                a.name AS asset_name,
                s.trade_date,
                s.month,
                s.settle,
                v.total_volume AS volume,
                v.at_close AS open_interest
            FROM assets a
            JOIN settlements s ON a.id = s.asset_id
            JOIN volume_oi v ON a.id = v.asset_id AND s.trade_date = v.trade_date AND s.month = v.month
            WHERE a.name = :asset_name AND s.trade_date = :trade_date
            """),
            {'asset_name': asset_name, 'trade_date': trade_date}
        ).fetchall()

        return [FuturesDataEntity.from_db_row(row) for row in result]
