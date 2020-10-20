import os
from functools import wraps

if os.getenv('SHARED_MEMORY_USE_LOCK') == '1':
    from multiprocessing import Lock
else:

    class Lock:  # type: ignore
        def acquire(self):
            pass

        def release(self):
            pass


_lock = Lock()


def lock(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _lock.acquire()
        try:
            return func(*args, **kwargs)
        finally:
            _lock.release()

    return wrapper
