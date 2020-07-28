import os
from functools import wraps

if os.getenv('SHARED_MEMORY_USE_UWSGI_LOCK') == '1':
    from uwsgidecorators import lock
else:

    def _dummy_lock(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    lock = _dummy_lock
