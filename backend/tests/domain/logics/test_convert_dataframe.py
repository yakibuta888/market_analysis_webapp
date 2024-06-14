# tests/domain/logics/test_convert_dataframe.py
import pandas as pd
import numpy as np
from src.domain.logics.convert_dataframe import dataframe_to_json, to_year_month_format

def test_dataframe_to_json():
    # テスト用のDataFrameを作成
    data = {
        'column1': [1, 2, 3],
        'column2': ['a', 'b', 'c']
    }
    df = pd.DataFrame(data)

    # 関数の実行
    result = dataframe_to_json(df)

    # 期待値
    expected_result = {
        "data": [
            {"column1": 1, "column2": 'a'},
            {"column1": 2, "column2": 'b'},
            {"column1": 3, "column2": 'c'}
        ]
    }

    # 結果の検証
    assert result == expected_result, "dataframe_to_json does not return expected JSON object."


def test_to_year_month_format():
    # テスト用のDataFrameを作成
    rng = pd.date_range('2021-01-01', periods=3, freq='ME')
    df = pd.DataFrame({ 'date': rng })

    # 関数の実行
    result_df = to_year_month_format(df, 'date')

    # 期待値
    expected_dates = ['2021-01', '2021-02', '2021-03']

    # 結果の検証
    assert np.array_equal(result_df['date'], expected_dates), "Column not converted to year-month format as expected."
