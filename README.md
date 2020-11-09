# Shared Memory Dict
A very simple [shared memory](https://docs.python.org/3/library/multiprocessing.shared_memory.html) dict implementation.

**Requires**: Python >= 3.8

```python
>> from shared_memory_dict import SharedMemoryDict
>> smd = SharedMemoryDict(name='tokens', size=1024)
>> smd['some-key'] = 'some-value-with-any-type'
>> smd['some-key']
'some-value-with-any-type'
```

> The arg `name` defines the location of the memory block, so if you want to share the memory between process use the same name

## Installation
Using `pip`:
```shell
pip install shared-memory-dict
```

## Locks
To use [multiprocessing.Lock](https://docs.python.org/3.8/library/multiprocessing.html#multiprocessing.Lock) on write operations of shared memory dict set environment variable `SHARED_MEMORY_USE_LOCK=1`.

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
