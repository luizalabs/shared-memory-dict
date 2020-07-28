import pytest

from shared_memory_dict import SharedMemoryDict


class TestSharedMemoryDict:
    @pytest.fixture
    def shared_memory_dict(self):
        smd = SharedMemoryDict(name='unit-tests', size=64)
        yield smd
        smd.clear()
        smd.cleanup()

    @pytest.fixture
    def key(self):
        return 'fake-key'

    @pytest.fixture
    def value(self):
        return 'fake-value'

    def test_should_add_a_key(self, shared_memory_dict, key, value):
        try:
            shared_memory_dict[key] = value
        except Exception as e:
            pytest.fail(f'Its should not raises: {e}')

    def test_should_read_a_key(self, shared_memory_dict, key, value):
        shared_memory_dict[key] = value
        assert shared_memory_dict[key] == value

    def test_should_read_a_key_with_default(
        self, shared_memory_dict, key, value
    ):
        default_value = 'default_value'
        assert shared_memory_dict.get(key, default_value) == default_value

    def test_should_read_a_key_without_default(
        self, shared_memory_dict, key, value
    ):
        assert shared_memory_dict.get(key) is None

    def test_should_remove_a_key(self, shared_memory_dict, key, value):
        shared_memory_dict[key] = value
        try:
            del shared_memory_dict[key]
        except Exception as e:
            pytest.fail(f'Its should not raises: {e}')

        with pytest.raises(KeyError):
            shared_memory_dict[key]

    def test_should_get_len_of_dict(self, shared_memory_dict, key, value):
        assert len(shared_memory_dict) == 0
        shared_memory_dict[key] = value
        assert len(shared_memory_dict) == 1

    def test_should_popitem(self, shared_memory_dict, key, value):
        shared_memory_dict[key] = value
        assert shared_memory_dict.popitem() == (key, value)

    def test_should_clear_dict(self, shared_memory_dict, key, value):
        shared_memory_dict[key] = value
        try:
            shared_memory_dict.clear()
        except Exception as e:
            pytest.fail(f'Its should not raises: {e}')

        with pytest.raises(KeyError):
            shared_memory_dict[key]

    def test_should_finalize_dict(self):
        smd = SharedMemoryDict(name='unit-tests', size=64)
        try:
            del smd
        except Exception as e:
            pytest.fail(f'Its should not raises: {e}')

    def test_should_check_item_in_dict(self, shared_memory_dict, key, value):
        shared_memory_dict[key] = value
        assert (key in shared_memory_dict) is True
        assert ('some-another-key' in shared_memory_dict) is False

    def test_should_return_dict_keys(self, shared_memory_dict, key, value):
        shared_memory_dict[key] = value
        assert list(shared_memory_dict.keys()) == [key]
