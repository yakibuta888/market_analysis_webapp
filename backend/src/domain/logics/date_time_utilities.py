# src/domain/logics/date_time_utilities.py
from datetime import datetime
import pytz

def parse_datetime(date_str: str) -> datetime:
    # 日時フォーマットの定義
    date_format = '%d %b %Y %I:%M:%S %p CT'
    try:
        # 日時文字列をパースする
        parsed_date = datetime.strptime(date_str, date_format)
        # タイムゾーンをCentral Timeに設定し、UTCに変換
        central = pytz.timezone('America/Chicago')
        date_with_timezone = central.localize(parsed_date)
        date_in_utc = date_with_timezone.astimezone(pytz.utc)
        return date_in_utc
    except ValueError as e:
        # 不適切な日付フォーマットの場合のエラーハンドリング
        raise ValueError(f"日付フォーマットが正しくありません: {date_str}。期待されるフォーマット: 'DD MMM YYYY HH:MM:SS AM/PM CT'。詳細: {str(e)}")
