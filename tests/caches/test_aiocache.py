import pytest

from shared_memory_dict import SharedMemoryDict
from shared_memory_dict.caches.aiocache import SharedMemoryCache


@pytest.mark.asyncio
class TestAioCache:

    @pytest.fixture
    async def backend(self):
        cache = SharedMemoryCache(name='ut', size=1024)
        yield cache
        await cache.clear()

    @pytest.fixture
    def key(self):
        return 'some-key'

    @pytest.fixture
    def value(self):
        return 'some-value'

    async def test_cache_instance_is_shared_memory_dict(self, backend):
        assert isinstance(backend._cache, SharedMemoryDict) is True

    async def test_should_add_value(self, backend, key, value):
        assert await backend.add(key, value) is True
        assert await backend.get(key) == value

    async def test_should_not_add_value_if_already_exists(self, backend, key, value):
        await backend.set(key, value)
        with pytest.raises(ValueError):
            await backend.add(key, value)

    @pytest.mark.parametrize('value', (
        'string', 1, {'some': 'dict'}, ['some', 'list']
    ))
    async def test_should_set_and_get_value(self, backend, key, value):
        try:
            await backend.set(key, value)
        except Exception as e:
            pytest.fail(f'Its should not raises: {e}')

        assert await backend.get(key) == value

    async def test_should_increment_value(self, backend, key):
        assert await backend.increment(key) == 1
        assert await backend.increment(key) == 2
        assert await backend.increment(key, delta=2) == 4

    async def test_should_delete_a_key(self, backend, key):
        await backend.set(key, 'fake')
        try:
            await backend.delete(key)
        except Exception as e:
            pytest.fail(f'Its should not raises: {e}')
        assert await backend.get(key) is None

    def test_should_call_parse_uri_path_without_errors(self, backend):
        assert backend.parse_uri_path('some/fake/path') == {}

    async def test_should_get_multi_values(self, backend):
        await backend.set('key-1', 1)
        await backend.set('key-2', 2)

        assert await backend.multi_get(['key-1', 'key-2']) == [1, 2]

    async def test_should_set_multi_values(self, backend):
        await backend.multi_set([('key-1', 1), ('key-2', 2)])
        assert await backend.get('key-1') == 1
        assert await backend.get('key-2') == 2

    async def test_should_check_if_a_keys_exists(self, backend, key, value):
        assert await backend.exists(key) is False

        await backend.set(key, value)
        assert await backend.exists(key) is True

    async def test_should_clear_cache(self, backend, key, value):
        await backend.set(key, value)
        assert await backend.clear() is True
        assert await backend.get(key) is None

    async def test_should_set_a_key_with_ttl(self, backend, key, value):
        assert await backend.set(key, value, ttl=1) is True
        # perform test two times to check class behavior
        assert await backend.set(key, value, ttl=1) is True

    async def test_should_delete_a_key_with_ttl(self, backend, key, value):
        assert await backend.set(key, value, ttl=1) is True
        assert await backend.delete(key) == 1

    async def test_should_raise_value_error_to_increment_on_a_non_number(
        self, backend, key
    ):
        await backend.set(key, 'value')
        with pytest.raises(TypeError):
            await backend.increment(key)

    async def test_should_delete_keys_with_namespace(self, key):
        expected_value = 1
        backend = SharedMemoryCache(namespace='prefix')

        await backend.set(key, expected_value)
        assert await backend.delete(key, namespace='another_prefix') == 0
        assert await backend.delete(key) == 1

        assert await backend.get(key) is None

    async def test_should_clean_keys_of_a_namespace(self, backend):
        assert await backend.set('without-namespace', 1) == 1
        assert await backend.set('with-namespace', 1, namespace='ut') == 1

        assert await backend.clear(namespace='ut') is True
        assert await backend.get('without-namespace') == 1
        assert await backend.get('with-namespace', namespace='ut') is None

    async def test_should_check_if_a_invalid_key_is_expired(self, backend):
        assert await backend.expire('fake', ttl=1) is False

    async def test_should_check_if_a_key_is_expired(self, backend, key, value):
        await backend.set(key, value)
        assert await backend.expire(key, ttl=None) is True

    async def test_should_expire_a_key(self, backend, key, value):
        await backend.set(key, value, ttl=1)
        assert await backend.expire(key, ttl=2) is True
