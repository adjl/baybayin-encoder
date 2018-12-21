import functools

from collections import deque


def preprocess_input(_func=None, transform=lambda x: x):
    def _preprocess_input(func):
        @functools.wraps(func)
        def __preprocess_input(inputs):
            if not inputs:
                return []
            return list(func(deque(map(transform, inputs))))
        return __preprocess_input
    if _func is None:
        return _preprocess_input
    return _preprocess_input(_func)
