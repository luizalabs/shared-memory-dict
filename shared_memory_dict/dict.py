import pickle
from collections import OrderedDict
from contextlib import contextmanager
from multiprocessing.shared_memory import SharedMemory
from typing import Any, Generator, KeysView, Optional

from .lock import lock
from .templates import MEMORY_NAME


class SharedMemoryDict(OrderedDict):
    def __init__(self, name: str, size: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._memory_block = self._get_or_create_memory_block(
            MEMORY_NAME.format(name=name), size
        )

    def cleanup(self) -> None:
        self._memory_block.close()

    def move_to_end(self, key: str, last: Optional[bool] = True) -> None:
        with self._modify_db() as db:
            db.move_to_end(key, last=last)

    @lock
    def clear(self) -> None:
        self._save_memory(OrderedDict())

    def popitem(self, last: Optional[bool] = True) -> Any:
        with self._modify_db() as db:
            return db.popitem(last)

    @contextmanager
    @lock
    def _modify_db(self) -> Generator:
        db = self._read_memory()
        yield db
        self._save_memory(db)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self._read_memory().get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._read_memory()[key]

    def __setitem__(self, key: str, value: Any) -> None:
        with self._modify_db() as db:
            db[key] = value

    def __len__(self) -> int:
        return len(self._read_memory())

    def __delitem__(self, key: str) -> None:
        with self._modify_db() as db:
            del db[key]

    def __del__(self) -> None:
        self.cleanup()

    def __contains__(self, key: object) -> bool:
        return key in self._read_memory()

    def keys(self) -> KeysView[Any]:  # type: ignore
        return self._read_memory().keys()

    def _get_or_create_memory_block(
        self, name: str, size: int
    ) -> SharedMemory:
        try:
            return SharedMemory(name=name)
        except FileNotFoundError:
            return SharedMemory(name=name, create=True, size=size)

    def _save_memory(self, db: OrderedDict) -> None:
        data = pickle.dumps(db, pickle.HIGHEST_PROTOCOL)
        self._memory_block.buf[: len(data)] = data  # type: ignore

    def _read_memory(self) -> OrderedDict:
        try:
            return pickle.loads(self._memory_block.buf)
        except pickle.UnpicklingError:
            return OrderedDict()
