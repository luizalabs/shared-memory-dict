# Shared Memory Dict
A very simple [shared memory](https://docs.python.org/3/library/multiprocessing.shared_memory.html) dict implementation.

**Require**: Python >=3.8

```python
>> from shared_memory_dict import SharedMemoryDict
>> smd = SharedMemoryDict(name='tokens', size=1024)
>> smd['some-key'] = 'some-value-with-any-type'
>> smd['some-key']
'some-value-with-any-type'
```

> The arg `name` defines the location of the memory block, so if you want to share the memory between process use the same name

To use [uwsgidecorators.lock](https://uwsgi-docs.readthedocs.io/en/latest/PythonDecorators.html#uwsgidecorators.lock) on write operations of shared memory dict set environment variable `SHARED_MEMORY_USE_UWSGI_LOCK`.

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

> This implementation is very based on django [LocMemCache](https://docs.djangoproject.com/en/3.0/topics/cache/#local-memory-caching)


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
