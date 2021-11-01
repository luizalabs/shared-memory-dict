import pytest

from shared_memory_dict.serializers import JSONSerializer, PickleSerializer


class TestPickleSerializer:
    @pytest.fixture
    def pickle_serializer(self):
        return PickleSerializer(None)

    @pytest.fixture
    def bytes_content(self):
        return (
            b'\x80\x05\x95\x12\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x03key'
            b'\x94\x8c\x05value\x94s.'
        )

    @pytest.fixture
    def dict_content(self):
        return {"key": "value"}

    def test_loads_should_transform_bytes_into_dict(
        self, pickle_serializer, bytes_content, dict_content
    ):
        assert pickle_serializer.loads(bytes_content) == dict_content

    def test_dumps_should_transform_dict_into_bytes(
        self, pickle_serializer, bytes_content, dict_content
    ):
        assert pickle_serializer.dumps(dict_content) == bytes_content


class TestJSONSerializer:
    @pytest.fixture
    def json_serializer(self):
        return JSONSerializer(None)

    @pytest.fixture
    def bytes_content(self):
        return b'{"key": "value"}\x00'

    @pytest.fixture
    def dict_content(self):
        return {"key": "value"}

    def test_loads_should_transform_bytes_into_dict(
        self, json_serializer, bytes_content, dict_content
    ):
        assert json_serializer.loads(bytes_content) == dict_content

    def test_dumps_should_transform_dict_into_bytes(
        self, json_serializer, bytes_content, dict_content
    ):
        assert json_serializer.dumps(dict_content) == bytes_content
