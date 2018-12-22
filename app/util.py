import functools

from collections import deque


def dequeify_input(_func=None, transform=lambda x: x):
    def _dequeify_input(func):
        @functools.wraps(func)
        def __dequeify_input(inputs):
            if not inputs:
                return []
            return list(func(deque(map(transform, inputs))))
        return __dequeify_input
    if _func is None:
        return _dequeify_input
    return _dequeify_input(_func)
