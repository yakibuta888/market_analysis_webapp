# src/domain/logics/validate_price_format.py
import re

def validate_price_format(value: str) -> bool:
    # 正規表現を用いて、許可される価格フォーマットに一致するか検証
    # カンマ入り数値、分数部分、'A'または'B'の接尾辞も許容する
    pattern = re.compile(
        r"^(?:\+|-)?(?:\d{1,3}(?:,\d{3})*|\d*)(?:'\d{1,3})?(?:\.\d+)?([AB]?)$"
    )

    if not pattern.match(value):
        raise ValueError(f"Invalid price format: {value}")

    # カンマを含む場合、正しい桁数で区切られているか追加で検証
    if "," in value:
        value = value.strip("AB")
        # 小数点や分数部分を考慮してカンマで分割
        numeric_part = value.split('.')[0]  # 小数点で分割して整数部分のみ取得
        numeric_part = numeric_part.split("'")[0]  # 分数記号で分割して最初の部分のみ取得
        parts = numeric_part.split(",")
        # 最初の数値部分は1～3桁である必要がある
        if len(parts[0]) < 1 or len(parts[0]) > 3:
            raise ValueError("Invalid number of digits before the first comma.")
        # それ以降の部分が全て3桁であることを検証
        if any(len(part) != 3 for part in parts[1:]):
            raise ValueError("Commas must be followed by three digits.")

    # 分数部分があるが、分数値がないケースの検証 ('5'' や '-5'' など)
    if "'" in value:
        parts = value.split("'")
        if len(parts) > 1 and not parts[1]:
            raise ValueError("Fraction part is missing.")

    # 特定の不正な値 ('abc' など) の検証
    if value.lower().isalpha():
        raise ValueError("Value cannot be purely alphabetical.")

    return True
