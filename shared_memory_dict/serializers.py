import json
import pickle
from typing import Protocol


class SharedMemoryDictSerializer(Protocol):
    def dumps(self, obj: dict) -> bytes:
        ...

    def loads(self, data: bytes) -> dict:
        ...


class JSONSerializer:
    def dumps(self, obj: dict) -> bytes:
        return json.dumps(obj).encode()

    def loads(self, data: bytes) -> dict:
        return json.loads(data)


class PickleSerializer:
    def dumps(self, obj: dict) -> bytes:
        return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)

    def loads(self, data: bytes) -> dict:
        return pickle.loads(data)
