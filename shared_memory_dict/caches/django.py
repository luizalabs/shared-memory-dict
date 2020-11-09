from time import time
from typing import Any, Dict, Optional, Tuple

from django.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache

from ..dict import SharedMemoryDict

_caches: Dict[str, SharedMemoryDict] = {}


class SharedMemoryCache(BaseCache):
    """
    A Django Cache implementation of SharedMemoryDict

    Values are stored as tuple with (`value`, `expiration time`)
    """

    def __init__(self, name: str, params: Dict) -> None:
        super().__init__(params=params)
        options = params.get('OPTIONS', {})
        self._cache = _caches.get(
            name,
            SharedMemoryDict(name, options.get('MEMORY_BLOCK_SIZE', 1024)),
        )

    def add(
        self,
        key: str,
        value: Any,
        timeout: Optional[int] = DEFAULT_TIMEOUT,
        version: Optional[int] = None,
    ):
        key = self.make_key(key, version=version)
        if self._get(key) is None:
            self._set(key, value, timeout)
            return True
        return False

    def get(
        self,
        key: str,
        default: Optional[Any] = None,
        version: Optional[int] = None,
    ):
        key = self.make_key(key, version=version)

        data = self._get(key)
        if data is None:
            return default

        return data[0]

    def set(
        self,
        key: str,
        value: Any,
        timeout: Optional[int] = DEFAULT_TIMEOUT,
        version: Optional[int] = None,
    ):
        key = self.make_key(key, version=version)
        self._set(key, value, timeout)

    def incr(
        self, key: str, delta: Optional[int] = 1, version: Optional[int] = None
    ):
        key = self.make_key(key, version=version)

        data = self._get(key)
        if data is None:
            raise ValueError(f'Key "{key}" not found')

        value, exp = data
        if not isinstance(value, int):
            raise TypeError(f'Expected an integer value but has: {value}')

        delta = delta or 1
        new_value = value + delta

        self._cache[key] = (new_value, exp)
        return new_value

    def delete(self, key: str, version: Optional[int] = None) -> None:
        key = self.make_key(key, version=version)
        return self._delete(key)

    def clear(self):
        self._cache.clear()

    def _get(self, key: str) -> Optional[Tuple[Any, float]]:
        """
        This method will return a tuple with (value, expiration time)
        or will return None if key has expired
        """
        data = self._cache.get(key, (None, -1.0))
        if not isinstance(data, tuple) or len(data) != 2:
            data = (None, -1.0)
        value, exp = data
        if exp is not None and exp <= time():
            self._delete(key)
            return None
        return (value, exp)

    def _set(
        self, key: str, value: Any, timeout: Optional[int] = DEFAULT_TIMEOUT
    ):
        self._cache[key] = (value, self.get_backend_timeout(timeout))

    def _delete(self, key: str) -> None:
        try:
            del self._cache[key]
        except KeyError:
            pass
