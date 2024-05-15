#src/infrastructure/mysql/futures_data_trade_date_repository_mysql.py
from datetime import date

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain.entities.trade_date_entity import TradeDateEntity
from src.domain.repositories.trade_date_repository import TradeDateRepository


class FuturesDataTradeDateRepositoryMysql(TradeDateRepository):
    def __init__(self, session: Session):
        self.session = session

    def fetch_trade_dates(self, asset_name: str, start_date: date | None, end_date: date | None, skip: int, limit: int) -> list[TradeDateEntity]:
        query = """
            SELECT DISTINCT s.trade_date
            FROM settlements s
            JOIN volume_oi v ON s.asset_id = v.asset_id AND s.trade_date = v.trade_date AND s.month = v.month
            JOIN assets a ON s.asset_id = a.id
            WHERE a.name = :asset_name
        """
        params: dict[str, str | int | date] = {'asset_name': asset_name, 'limit': limit, 'skip': skip}

        if start_date and end_date:
            query += "  AND s.trade_date BETWEEN :start_date AND :end_date"
            params['start_date'] = start_date
            params['end_date'] = end_date
        elif start_date:
            query += "  AND s.trade_date >= :start_date"
            params['start_date'] = start_date
        elif end_date:
            query += "  AND s.trade_date <= :end_date"
            params['end_date'] = end_date

        query += """
            ORDER BY s.trade_date
            LIMIT :limit OFFSET :skip
        """
        result = self.session.execute(text(query), params).fetchall()

        return [TradeDateEntity.from_db_row(row) for row in result]
