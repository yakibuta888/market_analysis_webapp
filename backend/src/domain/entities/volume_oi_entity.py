# src/domain/entities/volume_oi_entity.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

from src.domain.helpers.dataclass import DataClassBase
from src.domain.value_objects.trade_date import TradeDate
from src.domain.value_objects.year_month import YearMonth
from src.infrastructure.database.models import VolumeOI as VolumeOIModel


@dataclass(frozen=True, eq=True)
class VolumeOIEntity(DataClassBase):
    id: int | None
    asset_id: int
    trade_date: TradeDate
    month: YearMonth
    globex: int | None
    open_outcry: int | None
    clear_port: int | None
    total_volume: int
    block_trades: int | None
    efp: int | None
    efr: int | None
    tas: int | None
    deliveries: int | None
    at_close: int
    change: int | None

    def __post_init__(self):
        self._validate_positive_integers()

    def _validate_positive_integers(self):
        for field in ['total_volume', 'at_close']:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValueError(f"{field} must be greater than or equal to 0.")

    @classmethod
    def new_entity(cls, asset_id: int, trade_date: str, month: str, **kwargs: int) -> VolumeOIEntity:
        # ここで、文字列からTradeDateやYearMonthオブジェクトを作成する処理を実装
        return cls(
            id=None,
            asset_id=asset_id,
            trade_date=TradeDate.from_string(trade_date),
            month=YearMonth.from_string(month),
            **kwargs
        )

# NOTE: volume_oiテーブルを単独で取得するケースが今のところないため、from_dbメソッドは実装していません。利用する場合はservice, repositoryも合わせて実装する必要があります。
    @classmethod
    def from_db(cls, db_row: VolumeOIModel) -> VolumeOIEntity:
        # ここで、データベースから取得した行をエンティティに変換する処理を実装
        return cls(
            id=db_row.id,
            asset_id=db_row.asset_id,
            trade_date=TradeDate(db_row.trade_date),
            month=YearMonth.from_db_format(db_row.month),
            globex=db_row.globex,
            open_outcry=db_row.open_outcry,
            clear_port=db_row.clear_port,
            total_volume=db_row.total_volume,
            block_trades=db_row.block_trades,
            efp=db_row.efp,
            efr=db_row.efr,
            tas=db_row.tas,
            deliveries=db_row.deliveries,
            at_close=db_row.at_close,
            change=db_row.change,
        )
