import functools

from collections import deque


def transform_args(transform=lambda x: x, seq=deque):
    def _transform_args(func):
        @functools.wraps(func)
        def __transform_args(inputs):
            if not inputs:
                return []
            return list(func(seq(map(transform, inputs))))
        return __transform_args
    return _transform_args
