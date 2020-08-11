from unittest.mock import patch

from shared_memory_dict.hooks import create_shared_memory, free_shared_memory
from shared_memory_dict.templates import MEMORY_NAME


class TestHooks:

    def test_should_create_shared_memory(self):
        expected_name = 'unit-test'
        expected_size = 64

        with patch('shared_memory_dict.hooks.SharedMemory') as mock:
            create_shared_memory(expected_name, expected_size)

        mock.assert_called_once_with(
            MEMORY_NAME.format(name=expected_name),
            create=True,
            size=expected_size
        )

    def test_should_free_shared_memory(self):
        expected_name = 'unit-test'

        with patch('shared_memory_dict.hooks.SharedMemory') as mock:
            free_shared_memory(expected_name)

        mock.assert_called_once_with(MEMORY_NAME.format(name=expected_name))
        mock.return_value.unlink.assert_called_once()
