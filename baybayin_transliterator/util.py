import functools

from collections import deque


def transform_args(transform=lambda x: x, seq_in=deque, seq_out=tuple):
    def _transform_args(func):
        @functools.wraps(func)
        def __transform_args(inputs):
            if not inputs:
                return seq_out(inputs)
            return seq_out(func(seq_in(transform(x) for x in inputs)))
        return __transform_args
    return _transform_args
