# Shared Memory Dict

A very simple [shared memory](https://docs.python.org/3/library/multiprocessing.shared_memory.html) dict implementation.

**Requires**: Python >= 3.8

```python
>>> # In the first Python interactive shell
>> from shared_memory_dict import SharedMemoryDict
>> smd = SharedMemoryDict(name='tokens', size=1024)
>> smd['some-key'] = 'some-value-with-any-type'
>> smd['some-key']
'some-value-with-any-type'

>>> # In either the same shell or a new Python shell on the same machine
>> existing_smd = SharedMemoryDict(name='tokens', size=1024)
>>> existing_smd['some-key']
'some-value-with-any-type'
>>> existing_smd['new-key'] = 'some-value-with-any-type'


>>> # Back in the first Python interactive shell, smd reflects this change
>> smd['new-key']
'some-value-with-any-type'

>>> # Clean up from within the second Python shell
>>> existing_smd.shm.close()  # or "del existing_smd"

>>> # Clean up from within the first Python shell
>>> smd.shm.close()
>>> smd.shm.unlink()  # Free and release the shared memory block at the very end
>>> del smd  # use of smd after call unlink() is unsupported
```

> The arg `name` defines the location of the memory block, so if you want to share the memory between process use the same name.
> The size (in bytes) occupied by the contents of the dictionary depends on the serialization used in storage. By default pickle is used.

## Installation

Using `pip`:

```shell
pip install shared-memory-dict
```

## Locks

To use [multiprocessing.Lock](https://docs.python.org/3.8/library/multiprocessing.html#multiprocessing.Lock) on write operations of shared memory dict set environment variable `SHARED_MEMORY_USE_LOCK=1`.

## Serialization

We use [pickle](https://docs.python.org/3/library/pickle.html) as default to read and write the data into the shared memory block.

You can create a custom serializer by implementing the `dumps` and `loads` methods.

Custom serializers should raise `SerializationError` if the serialization fails and `DeserializationError` if the deserialization fails. Both are defined in the `shared_memory_dict.serializers` module.

An example of a JSON serializer extracted from serializers module:

```python
NULL_BYTE: Final = b"\x00"


class JSONSerializer:
    def dumps(self, obj: dict) -> bytes:
        try:
            return json.dumps(obj).encode() + NULL_BYTE
        except (ValueError, TypeError):
            raise SerializationError(obj)

    def loads(self, data: bytes) -> dict:
        data = data.split(NULL_BYTE, 1)[0]
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            raise DeserializationError(data)

```

Note: A null byte is used to separate the dictionary contents from the bytes that are in memory.

To use the custom serializer you must set it when creating a new shared memory dict instance:

```python
>>> smd = SharedMemoryDict(name='tokens', size=1024, serializer=JSONSerializer())
```

### Caveat

The pickle module is not secure. Only unpickle data you trust.

See more [here](https://docs.python.org/3/library/pickle.html).

## Django Cache Implementation

There's a [Django Cache Implementation](https://docs.djangoproject.com/en/3.0/topics/cache/) with Shared Memory Dict:

```python
# settings/base.py
CACHES = {
    'default': {
        'BACKEND': 'shared_memory_dict.caches.django.SharedMemoryCache',
        'LOCATION': 'memory',
        'OPTIONS': {'MEMORY_BLOCK_SIZE': 1024}
    }
}
```

**Install with**: `pip install "shared-memory-dict[django]"`

### Caveat

With Django cache implementation the keys only expire when they're read. Be careful with memory usage

## AioCache Backend

There's also a [AioCache Backend Implementation](https://aiocache.readthedocs.io/en/latest/caches.html) with Shared Memory Dict:

```python
From aiocache import caches

caches.set_config({
    'default': {
        'cache': 'shared_memory_dict.caches.aiocache.SharedMemoryCache',
        'size': 1024,
    },
})
```

> This implementation is very based on aiocache [SimpleMemoryCache](https://aiocache.readthedocs.io/en/latest/caches.html#simplememorycache)

**Install with**: `pip install "shared-memory-dict[aiocache]"`
