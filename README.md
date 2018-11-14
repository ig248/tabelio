[![Build Status](https://travis-ci.com/ig248/tabelio.svg?branch=master)](https://travis-ci.com/ig248/tabelio)
[![Coverage Status](https://codecov.io/gh/ig248/tabelio/branch/master/graph/badge.svg)](https://codecov.io/gh/ig248/tabelio)

# Tabelio - a set of IO tools for tabular data

Convert files between common tabular data formats.

- provides the `convert_table_file` python function
- provides the `csv2hdf` command line tool
- other command line tools planned

File formats are supported by defining a common interface for reading/writing/appending.

## Supported formats

Currently supported formats are: `csv`, `hdf` (`hdf-fixed`) and `hdf-table`.

## Limitations

Currently, the dataset must fit in memory to perform conversion. A chunked implementation will be added in the future.

Further formats to be added include Apache's `parquet` and web-friendly `json` (with `base64` encoding).

## Background

This is a small tool I wrote primarily for batch-converting `csv` files to `hdf`.
The need was inspired by the resulting performance gains for day-to-day data science work - as described
in [this blog post](https://ig248.gitlab.io/post/2018-11-06-table-formats/).
