import numpy as np
import pandas as pd

from . import ini

DEF_N = 48


def mock_datetime_range(*, periods=DEF_N, start=None, freq='0.5H'):
    """Sample datetime range."""
    start = start or pd.datetime.now()
    return pd.date_range(start=start, freq=freq, periods=periods)


def mock_table_data(
    *,
    rows=DEF_N,
    datetime_column=True,
    start_date=None,
    numeric_columns='abcdef'
):
    """Create mock DataFrame."""
    data = {}
    if datetime_column:
        datetimes = mock_datetime_range(periods=rows, start=start_date)
        data = {ini.Columns.datetime: datetimes}
    for column in numeric_columns:
        data[column] = np.random.rand(rows)
    df = pd.DataFrame(data)
    return df
