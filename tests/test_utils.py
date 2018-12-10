import pytest

from tabelio.mock import mock_table_data
from tabelio.utils import _ceil_div, PandasBatchGenerator


@pytest.mark.parametrize(
    'dividend, divisor, result', [
        (0, 1, 0),
        (0, 2, 0),
        (1, 1, 1),
        (1, 2, 1),
        (2, 2, 1),
        (2, 1, 2),
    ]
)
def test_ceil_div(dividend, divisor, result):
    assert _ceil_div(dividend, divisor) == result


class TestPandasBatchGenerator:
    @pytest.mark.parametrize(
        'n_rows, batch_size, expected_nb_batches', [
            (0, 2, 0),
            (1, 2, 1),
            (2, 2, 1),
            (4, 2, 2),
            (5, 2, 3),
        ]
    )
    def test_nb_batches(self, n_rows, batch_size, expected_nb_batches):
        df = mock_table_data(rows=n_rows)
        generator = PandasBatchGenerator(
            df=df, batch_size=batch_size
        )
        assert len(generator) == expected_nb_batches

    @pytest.mark.parametrize(
        'n_rows, batch_size, expected_last_batch_size',
        [(4, 2, 2), (5, 2, 1), (7, 3, 1)]
    )
    def test_batch_size(self, n_rows, batch_size, expected_last_batch_size):
        df = mock_table_data(rows=n_rows)
        generator = PandasBatchGenerator(df=df, batch_size=batch_size)
        for batch_id in range(len(generator) - 1):
            batch = generator[batch_id]
            assert len(batch) == batch_size

        assert len(generator[-1]) == expected_last_batch_size
