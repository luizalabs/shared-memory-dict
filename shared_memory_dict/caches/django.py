from time import time
from typing import Any, Dict, Optional

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
        self.validate_key(key)

        if self._has_expired(key):
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
        self.validate_key(key)

        if self._has_expired(key):
            self._delete(key)
            return default

        value, _ = self._cache[key]
        self._cache.move_to_end(key, last=False)

        return value

    def set(
        self,
        key: str,
        value: Any,
        timeout: Optional[int] = DEFAULT_TIMEOUT,
        version: Optional[int] = None,
    ):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        self._set(key, value, timeout)

    def incr(
        self, key: str, delta: Optional[int] = 1, version: Optional[int] = None
    ):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        if self._has_expired(key):
            self._delete(key)
            raise ValueError(f'Key "{key}" not found')

        value, expire_info = self._cache[key]
        new_value = value + delta

        self._cache[key] = (new_value, expire_info)
        self._cache.move_to_end(key, last=False)

        return new_value

    def delete(self, key: str, version: Optional[int] = None) -> None:
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return self._delete(key)

    def clear(self):
        self._cache.clear()

    def _has_expired(self, key: str) -> bool:
        value = self._cache.get(key, (None, -1))
        if not isinstance(value, tuple) or len(value) != 2:
            value = (None, -1)
        exp = value[1]
        return exp is not None and exp <= time()

    def _set(
        self, key: str, value: Any, timeout: Optional[int] = DEFAULT_TIMEOUT
    ):
        if len(self._cache) >= self._max_entries:
            self._cull()
        self._cache[key] = (value, self.get_backend_timeout(timeout))
        self._cache.move_to_end(key, last=False)

    def _delete(self, key: str) -> None:
        try:
            del self._cache[key]
        except KeyError:
            pass

    def _cull(self) -> None:
        if self._cull_frequency == 0:
            self._cache.clear()
        else:
            count = len(self._cache) // self._cull_frequency
            for _ in range(count):
                self._cache.popitem()
