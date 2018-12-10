import argparse

from .table import convert_table_file


def csv2hdf():
    parser = argparse.ArgumentParser(description='Convert CSV to HDF')
    parser.add_argument(dest='filename', help='input CSV file name')

    args = parser.parse_args()
    convert_table_file(
        filename=args.filename, from_format='csv', to_format='hdf',
        progress=True
    )
