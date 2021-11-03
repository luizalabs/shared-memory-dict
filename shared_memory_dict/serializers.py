import json
import pickle
from typing import Final, Protocol

NULL_BYTE: Final = b"\x00"


class SharedMemoryDictSerializer(Protocol):
    def dumps(self, obj: dict) -> bytes:
        ...

    def loads(self, data: bytes) -> dict:
        ...


class JSONSerializer:
    def dumps(self, obj: dict) -> bytes:
        return json.dumps(obj).encode() + NULL_BYTE

    def loads(self, data: bytes) -> dict:
        data = data.split(NULL_BYTE, 1)[0]
        return json.loads(data)


class PickleSerializer:
    def dumps(self, obj: dict) -> bytes:
        return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)

    def loads(self, data: bytes) -> dict:
        return pickle.loads(data)
