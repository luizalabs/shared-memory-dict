import asyncio
from asyncio.events import AbstractEventLoop, TimerHandle
from typing import Any, Dict, List, Optional, Tuple, Union

from aiocache.base import BaseCache
from aiocache.serializers import BaseSerializer, NullSerializer

from ..dict import SharedMemoryDict

Number = Union[int, float]


class SharedMemoryCache(BaseCache):
    """
    A AioCache implementation of SharedMemoryDict
    based on aiocache.backends.memory.SimpleMemoryCache
    """

    NAME = 'shared_memory'

    def __init__(
        self,
        serializer: Optional[BaseSerializer] = None,
        name: str = 'smc',
        size: int = 1024,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.serializer = serializer or NullSerializer()
        self._cache = SharedMemoryDict(name, size)
        self._handlers: Dict[str, TimerHandle] = {}

    @classmethod
    def parse_uri_path(cls, path: str) -> Dict:
        return {}

    async def _get(
        self, key: str, encoding: Optional[str] = 'utf-8', _conn=None
    ):
        return self._cache.get(key)

    async def _multi_get(
        self, keys: List[str], encoding: Optional[str] = 'utf-8', _conn=None
    ):
        return [self._cache.get(key) for key in keys]

    async def _set(
        self,
        key: str,
        value: Any,
        ttl: Optional[Number] = None,
        _cas_token: Optional[Any] = None,
        _conn=None,
    ) -> bool:
        if _cas_token is not None and _cas_token != self._cache.get(key):
            return False

        if key in self._handlers:
            self._handlers[key].cancel()

        self._cache[key] = value
        if ttl:
            self._handlers[key] = self._loop().call_later(
                ttl, self._delete_key, key
            )

        return True

    async def _multi_set(
        self,
        pairs: Tuple[Tuple[str, Any]],
        ttl: Optional[Number] = None,
        _conn=None,
    ) -> bool:
        for key, value in pairs:
            await self._set(key, value, ttl=ttl)
        return True

    async def _add(
        self,
        key: str,
        value: Any,
        ttl: Optional[Number] = None,
        _conn=None,
    ):
        if key in self._cache:
            raise ValueError(
                f'Key {key} already exists, use .set to update the value'
            )

        await self._set(key, value, ttl=ttl)
        return True

    async def _exists(self, key: str, _conn=None):
        return key in self._cache

    async def _increment(self, key: str, delta: int, _conn=None):
        new_value = delta
        if key not in self._cache:
            self._cache[key] = delta
        else:
            value = self._cache[key]
            try:
                new_value = int(value) + delta
            except ValueError:
                raise TypeError('Value is not an integer') from None

        self._cache[key] = new_value
        return new_value

    async def _expire(
        self, key: str, ttl: Union[int, float], _conn=None
    ) -> bool:
        if key not in self._cache:
            return False

        handle = self._handlers.pop(key, None)

        if handle:
            handle.cancel()
        if ttl:
            self._handlers[key] = self._loop().call_later(
                ttl, self._delete_key, key
            )

        return True

    async def _delete(self, key: str, _conn=None) -> int:
        return self._delete_key(key)

    async def _clear(
        self, namespace: Optional[str] = None, _conn=None
    ) -> bool:
        if namespace:
            for key in self._cache.keys():
                if key.startswith(namespace):
                    self._delete_key(key)
        else:
            self._cache.clear()
            self._handlers = {}
        return True

    async def _redlock_release(self, key: str, value: Any) -> int:
        if self._cache.get(key) == value:
            self._cache.pop(key)
            return 1
        return 0

    def _delete_key(self, key: str) -> int:
        if self._cache.pop(key, None):
            handle = self._handlers.pop(key, None)
            if handle:
                handle.cancel()
            return 1
        return 0

    def _loop(self) -> AbstractEventLoop:
        return asyncio.get_event_loop()
