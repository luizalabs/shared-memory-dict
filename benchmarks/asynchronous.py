import asyncio
from string import ascii_lowercase
from timeit import timeit

from aiocache.backends.redis import RedisCache
from aiocache.backends.memory import SimpleMemoryCache
from shared_memory_dict.caches.aiocache import SharedMemoryCache

loop = asyncio.get_event_loop()

cache_smc_aiocache = SharedMemoryCache(size=64)
cache_aiocache_redis = RedisCache(loop=loop)
cache_aiocache_memory = SimpleMemoryCache()


async def agressive(cache):
    for c in ascii_lowercase:
        for i in range(5):
            await cache.set(f'{c}{i}', '1')
        for i in range(10, 0, -1):
            await cache.get(f'{c}{i}')


async def fun(cache):
    await cache.set('fun', 'uhull')
    for _ in range(3):
        await cache.get('fun')


def collect(cache_var_name):
    time_of_agressive = timeit(
        stmt=f'loop.run_until_complete(agressive({cache_var_name}))',
        number=100,
        globals=globals()
    )
    time_of_fun = timeit(
        stmt=f'loop.run_until_complete(fun({cache_var_name}))',
        number=100,
        globals=globals()
    )

    return {
        'agressive': time_of_agressive,
        'fun': time_of_fun
    }


if __name__ == '__main__':
    caches = {
        k: collect(k)
        for k in globals().keys()
        if k.startswith('cache_')
    }

    print('Bench Against Async Solutions')
    for k, v in caches.items():
        print(f'Cache Type : {k}:')
        print(f'agressive  : {v["agressive"]}')
        print(f'fun        : {v["fun"]}')
        print('')
