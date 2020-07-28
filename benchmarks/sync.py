from string import ascii_lowercase
from timeit import timeit

from django.core.cache.backends.locmem import LocMemCache
from django_redis.cache import RedisCache
from shared_memory_dict.caches.django import SharedMemoryCache

cache_smc_django = SharedMemoryCache(
    'django', params={'OPTIONS': {'MEMORY_BLOCK_SIZE': 64}}
)
cache_django_redis = RedisCache(server='redis://127.0.0.1:6379/1', params={})
cache_django_locmem = LocMemCache('locmem', params={})


def agressive(cache):
    for c in ascii_lowercase:
        for i in range(5):
            cache.set(f'{c}{i}', '1')
        for i in range(10, 0, -1):
            cache.get(f'{c}{i}')


def fun(cache):
    cache.set('fun', 'uhull')
    for _ in range(3):
        cache.get('fun')


def collect(cache_var_name):
    time_of_agressive = timeit(
        stmt=f'agressive({cache_var_name})', number=100, globals=globals()
    )
    time_of_fun = timeit(
        stmt=f'fun({cache_var_name})', number=100, globals=globals()
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

    print('Bench Against Sync Solutions')
    for k, v in caches.items():
        print(f'Cache Type : {k}:')
        print(f'agressive  : {v["agressive"]}')
        print(f'fun        : {v["fun"]}')
        print('')
