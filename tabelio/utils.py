def _ceil_div(dividend, divisor):
    return dividend // divisor + (1 if dividend % divisor else 0)


class Sequence(object):
    """Base object for an indexable iterable.

    Every `Sequence` must implement the `__getitem__` and
    the `__len__` methods.
    The method `__getitem__` should return a complete batch.

    https://github.com/keras-team/keras/blob/master/keras/utils/data_utils.py
    """

    def __getitem__(self, index):
        """Get batch at position `index`.

        # Arguments
            index: position of the chunk in the Sequence.
        # Returns
            A batch
        """
        raise NotImplementedError

    def __len__(self):
        """Get number of chunks in the Sequence.

        # Returns
            The number of chunks in the Sequence.
        """
        raise NotImplementedError

    def __iter__(self):
        """Create a generator that iterate over the Sequence."""
        for item in (self[i] for i in range(len(self))):
            yield item


class PandasBatchGenerator(Sequence):
    """Yield pd.DataFrame in batches as sub-frames."""

    def __init__(self, df, batch_size=None):
        self.df = df
        self.batch_size = batch_size

    def __len__(self):
        return _ceil_div(len(self.df), self.batch_size)

    def __getitem__(self, batch_idx):
        batch_idx = batch_idx % len(self)
        columns = self.df.columns
        batch_size = self.batch_size or len(self.df)
        batch_df = self.df[columns].iloc[batch_idx * batch_size:
                                         batch_idx * batch_size + batch_size]

        return batch_df
