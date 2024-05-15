# src/domain/logics/validate_trade_date.py
from datetime import datetime, date

from src.settings import logger

def validate_and_convert_trade_date(value: str | date | None) -> date | None:
    logger.debug(f"trade_dateの値を検証・変換します。value={value}")
    if value is None:
        return None
   
    if isinstance(value, str):
        try:
            # 文字列形式の取引日をdatetime.dateオブジェクトに変換
            parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as e:
            # ValueErrorを捕捉し、カスタムエラーメッセージを発生させる
            raise ValueError(f"trade_dateが無効な日付フォーマットです。YYYY-MM-DD形式である必要があります。: {value}") from e
    elif isinstance(value, date):  # type: ignore
        parsed_date = value
    else:
        raise TypeError(f"trade_datesの項目はstrまたはdate型である必要があります。: {type(value)}")

    if parsed_date > datetime.now().date():
        raise ValueError("取引日は過去または今日でなければなりません。")

    logger.debug(f"取引日を検証・変換しました。parsed_date={parsed_date}")
    return parsed_date
