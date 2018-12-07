import pandas as pd
import pytest

from tabelio.mock import mock_table_data
from tabelio.table import (FORMATS, BaseFormat, _find_format,
                           convert_table_file, read_table_format,
                           write_table_format)

KNOWN_EXT = 'csv'
UNKNOWN_EXT = 'unknown'


@pytest.fixture
def df():
    return mock_table_data(rows=3, start_date='2018-01-01')


@pytest.fixture
def double_df(df):
    ddf = pd.concat([df, df])
    ddf = ddf.reset_index(drop=True)
    return ddf


@pytest.fixture
def triple_df(df):
    ddf = pd.concat([df, df, df])
    ddf = ddf.reset_index(drop=True)
    return ddf


@pytest.fixture
def csv_file(df, tmpdir_factory):
    fn = str(tmpdir_factory.mktemp("data").join("temp.csv"))
    df.to_csv(fn, index=False)
    return fn


@pytest.mark.parametrize('method', ['read', 'write', 'append'])
def test_baseformat_is_abstract(method):
    with pytest.raises(NotImplementedError):
        getattr(BaseFormat, method)(df=None, filename=None)


def test_one_extension_known():
    assert KNOWN_EXT in FORMATS


@pytest.mark.parametrize('format, fmt_class', FORMATS.items())
class TestFormat:
    def test_format_is_valid(self, format, fmt_class):
        assert isinstance(format, str)
        assert issubclass(fmt_class, BaseFormat)

    def test_append_non_file(self, format, fmt_class, df, tmpdir_factory):
        filename = str(tmpdir_factory.mktemp("data").join(f'temp.{format}'))
        with pytest.raises(FileNotFoundError):
            fmt_class.append(df=df, filename=filename)

    def test_write_read(self, format, fmt_class, df, tmpdir_factory):
        filename = str(tmpdir_factory.mktemp("data").join(f'temp.{format}'))
        fmt_class.write(df=df, filename=filename)
        new_df = fmt_class.read(filename=filename)
        pd.testing.assert_frame_equal(new_df, df)

    def test_write_append_read(
        self, format, fmt_class, df, double_df, tmpdir_factory
    ):
        filename = str(tmpdir_factory.mktemp("data").join(f'temp.{format}'))
        fmt_class.write(df=df, filename=filename)
        fmt_class.append(df=df, filename=filename)
        new_df = fmt_class.read(filename=filename)
        pd.testing.assert_frame_equal(new_df, double_df)

    def test_write_append_x2_read(
        self, format, fmt_class, df, triple_df, tmpdir_factory
    ):
        filename = str(tmpdir_factory.mktemp("data").join(f'temp.{format}'))
        fmt_class.write(df=df, filename=filename)
        fmt_class.append(df=df, filename=filename)
        fmt_class.append(df=df, filename=filename)
        new_df = fmt_class.read(filename=filename)
        pd.testing.assert_frame_equal(new_df, triple_df)


class TestFindFormat:
    @pytest.mark.parametrize(
        'format, filename', [
            (UNKNOWN_EXT, f'file.{UNKNOWN_EXT}'),
            (UNKNOWN_EXT, f'file.{KNOWN_EXT}'), (None, f'file.{UNKNOWN_EXT}'),
            (UNKNOWN_EXT, None), (None, None)
        ]
    )
    def test_unknown_format_raises(self, format, filename):
        with pytest.raises(ValueError):
            _find_format(format=format, filename=filename)

    @pytest.mark.parametrize(
        'format, filename, expected_format', [
            (KNOWN_EXT, f'file.{UNKNOWN_EXT}', KNOWN_EXT),
            (None, f'file.{KNOWN_EXT}', KNOWN_EXT),
        ]
    )
    def test_format_found_correctly(self, format, filename, expected_format):
        found_format = _find_format(format=format, filename=filename)
        assert found_format == expected_format


@pytest.mark.parametrize('format', FORMATS.keys())
class TestReadWrite:
    def test_write_read(self, format, df, tmpdir_factory):
        filename = str(tmpdir_factory.mktemp("data").join(f'temp.{format}'))
        write_table_format(df=df, filename=filename)
        new_df = read_table_format(filename=filename)
        pd.testing.assert_frame_equal(new_df, df)

    def test_write_append_read(self, format, df, double_df, tmpdir_factory):
        filename = str(tmpdir_factory.mktemp("data").join(f'temp.{format}'))
        write_table_format(df=df, filename=filename)
        write_table_format(df=df, filename=filename, append=True)
        new_df = read_table_format(filename=filename)
        pd.testing.assert_frame_equal(new_df, double_df)

    def test_append_read(self, format, df, tmpdir_factory):
        filename = str(tmpdir_factory.mktemp("data").join(f'temp.{format}'))
        write_table_format(df=df, filename=filename, append=True)
        new_df = read_table_format(filename=filename)
        pd.testing.assert_frame_equal(new_df, df)


@pytest.mark.parametrize('to_format', FORMATS.keys())
def test_convert(df, csv_file, to_format):
    from_format = 'csv'
    from_file = csv_file
    to_file = convert_table_file(
        filename=csv_file, from_format=from_format, to_format=to_format
    )
    from_df = read_table_format(filename=from_file)
    to_df = read_table_format(filename=to_file)

    assert to_file.endswith(to_format)
    pd.testing.assert_frame_equal(to_df, from_df)
