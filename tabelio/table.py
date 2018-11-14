import os.path

import pandas as pd

from . import ini


class BaseFormat:
    @classmethod
    def read(cls, *, filename, **kwargs):
        raise NotImplementedError

    @classmethod
    def write(cls, *, df, filename, **kwargs):
        raise NotImplementedError

    @classmethod
    def append(cls, *, df, filename, **kwargs):
        raise NotImplementedError


class CSVFormat(BaseFormat):
    @classmethod
    def read(cls, *, filename, **kwargs):
        defaults = dict(parse_dates=[ini.Columns.datetime])
        kwargs = {**defaults, **kwargs}
        return pd.read_csv(filename, **kwargs)

    @classmethod
    def write(cls, *, df, filename, **kwargs):
        defaults = dict(index=False)
        kwargs = {**defaults, **kwargs}
        pd.DataFrame.to_csv(df, filename, **kwargs)

    @classmethod
    def append(cls, *, df, filename, **kwargs):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f'{filename} must be an existing file.')
        defaults = dict(mode='a', header=False)
        kwargs = {**defaults, **kwargs}
        cls.write(df=df, filename=filename, **kwargs)


class HDFFixedFormat(BaseFormat):
    @classmethod
    def read(cls, *, filename, **kwargs):
        defaults = {}
        kwargs = {**defaults, **kwargs}
        return pd.read_hdf(filename, **kwargs)

    @classmethod
    def write(cls, *, df, filename, **kwargs):
        df = df.reset_index(drop=True)
        defaults = dict(key='data', format='fixed')
        kwargs = {**defaults, **kwargs}
        pd.DataFrame.to_hdf(df, filename, **kwargs)

    @classmethod
    def append(cls, *, df, filename, **kwargs):
        """Append by reading in data first."""
        existing_df = cls.read(filename=filename)
        df = pd.concat([existing_df, df], axis=0)
        cls.write(df=df, filename=filename, **kwargs)


class HDFTableFormat(BaseFormat):
    @classmethod
    def read(cls, *, filename, **kwargs):
        defaults = {}
        kwargs = {**defaults, **kwargs}
        return pd.read_hdf(filename, **kwargs)

    @classmethod
    def write(cls, *, df, filename, **kwargs):
        df = df.reset_index(drop=True)
        defaults = dict(key='data', format='table')
        kwargs = {**defaults, **kwargs}
        pd.DataFrame.to_hdf(df, filename, **kwargs)

    @classmethod
    def append(cls, *, df, filename, **kwargs):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f'{filename} must be an existing file.')
        defaults = dict(key='data', format='table', append=True)
        kwargs = {**defaults, **kwargs}
        # Continue indexing from last value in file
        # Otherwise, HDFStore re-starts index at 0
        start_index = pd.read_hdf(filename, start=-1).index[-1] + 1
        df = df.reset_index(drop=True)
        df.index += start_index
        pd.DataFrame.to_hdf(df, filename, **kwargs)


FORMATS = {
    'csv': CSVFormat,
    'hdf': HDFFixedFormat,
    'hdf-fixed': HDFFixedFormat,
    'hdf-table': HDFTableFormat,
}


def _find_format(*, format, filename):
    """Resolve file format from file extension."""
    if filename:
        _, ext = os.path.splitext(filename)
        ext = ext.lstrip('.')
    else:
        ext = None
    if not format:
        if ext in FORMATS.keys():
            format = ext
        else:
            raise ValueError(
                f'Unknown file extension "{ext}"; '
                f'specify `format` explicitly'
            )
    elif format not in FORMATS.keys():
        raise ValueError(f'Unknown table format "{format}"')
    return format


def read_table_format(*, filename, format=None, **kwargs):
    format = _find_format(format=format, filename=filename)
    df = FORMATS[format].read(filename=filename, **kwargs)
    return df


def write_table_format(*, df, filename, format=None, append=False, **kwargs):
    format = _find_format(format=format, filename=filename)
    if append:
        FORMATS[format].append(df=df, filename=filename, **kwargs)
    else:
        FORMATS[format].write(df=df, filename=filename, **kwargs)
    return filename


def convert_table_file(
    *, filename, from_format=None, to_format, from_kwargs=None, to_kwargs=None
):
    """Convert table file on disk between formats."""
    basename, from_ext = os.path.splitext(filename)
    to_filename = f'{basename}.{to_format}'
    from_kwargs = from_kwargs or {}
    to_kwargs = to_kwargs or {}
    df = read_table_format(
        filename=filename, format=from_format, **from_kwargs
    )
    return write_table_format(
        df=df, filename=to_filename, format=to_format, **to_kwargs
    )
