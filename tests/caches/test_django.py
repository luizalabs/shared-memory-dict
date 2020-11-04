import pytest

from shared_memory_dict import SharedMemoryDict
from shared_memory_dict.caches.django import SharedMemoryCache


class TestDjangoSharedMemoryCache:

    @pytest.fixture
    def backend(self):
        cache = SharedMemoryCache(name='ut', params={})
        yield cache
        cache.clear()

    @pytest.fixture
    def key(self):
        return 'some-key'

    @pytest.fixture
    def value(self):
        return 'some-value'

    def test_cache_instance_is_shared_memory_dict(self, backend):
        assert isinstance(backend._cache, SharedMemoryDict) is True

    def test_should_add_value(self, backend, key, value):
        assert backend.add(key, value) is True
        assert backend.get(key) == value

    def test_should_not_add_value_if_already_exists(self, backend, key, value):
        backend.set(key, value)
        assert backend.add(key, value) is False

    @pytest.mark.parametrize('value', (
        'string', 1, 0.300, {'some': 'dict'}, ['some', 'list']
    ))
    def test_should_set_and_get_value(self, backend, value):
        key = 'some-key'
        try:
            backend.set(key, value)
        except Exception as e:
            pytest.fail(f'Its should not raises: {e}')

        assert backend.get(key) == value

    def test_should_set_and_get_value_with_timeout(self, backend, value):
        key = 'some-key'
        value = 2
        try:
            backend.set(key, value, 2)
        except Exception as e:
            pytest.fail(f'Its should not raises: {e}')

        assert backend.get(key) == value


    def test_get_a_non_exists_key_with_default_value(self, backend):
        expected_value = 'some-random-value'
        assert backend.get(
            'some-random-key',
            default=expected_value
        ) == expected_value

    def test_should_incr_value(self, backend, key):
        backend.add(key, 0)
        assert backend.incr(key) == 1
        assert backend.incr(key) == 2

    def test_should_raise_key_error_on_incr_a_non_exists_key(self, backend):
        with pytest.raises(ValueError):
            backend.incr('some-random-key')

    def test_should_delete_a_key(self, backend, key):
        backend.set(key, 'fake')
        try:
            backend.delete(key)
        except Exception as e:
            pytest.fail(f'Its should not raises: {e}')
        assert backend.get(key) is None

    def test_should_cull_cache_with_frequency(self):
        backend = SharedMemoryCache(
            name='smc',
            params={'OPTIONS': {'MAX_ENTRIES': 2, 'CULL_FREQUENCY': 2}}
        )
        for i in range(3):
            backend.set(f'key-{i}', i)

        assert backend.get('key-2') == 2
        assert backend.get('key-1') == 1
        assert backend.get('key-0') is None

    def test_should_cull_cache_without_frequency(self):
        backend = SharedMemoryCache(
            name='smc',
            params={'OPTIONS': {'MAX_ENTRIES': 2, 'CULL_FREQUENCY': 0}}
        )
        for i in range(3):
            backend.set(f'key-{i}', i)

        assert backend.get('key-2') == 2
        assert backend.get('key-1') is None
        assert backend.get('key-0') is None

    @pytest.mark.parametrize('value', ('fake', ('fake',), {}))
    def test_should_prevent_key_error_for_invalid_exp_info(
        self, backend, key, value
    ):
        formated_key = backend.make_key(key, version=None)
        backend._cache[formated_key] = value
        assert backend.get(key) is None

    def test_should_raise_error_for_non_int_values_on_incr(self, backend, key):
        backend.set(key, 'a')
        with pytest.raises(TypeError):
            backend.incr(key)
