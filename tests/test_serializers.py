import pytest

from shared_memory_dict.serializers import (
    JSONSerializer,
    PickleSerializer,
    SerializationError,
    DeserializationError,
)


class TestPickleSerializer:
    @pytest.fixture
    def pickle_serializer(self):
        return PickleSerializer()

    @pytest.fixture
    def bytes_content(self):
        return (
            b'\x80\x05\x95\x12\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x03key'
            b'\x94\x8c\x05value\x94s.'
        )

    @pytest.fixture
    def dict_content(self):
        return {"key": "value"}

    @pytest.fixture
    def dict_not_serializable(self):
        class C:
            def __reduce__(self):
                return (C, None)

        return {"key": C()}

    @pytest.fixture
    def bytes_content_with_invalid_pickle(self):
        return b'not pickle'

    def test_loads_should_transform_bytes_into_dict(
        self, pickle_serializer, bytes_content, dict_content
    ):
        assert pickle_serializer.loads(bytes_content) == dict_content

    def test_dumps_should_transform_dict_into_bytes(
        self, pickle_serializer, bytes_content, dict_content
    ):
        assert pickle_serializer.dumps(dict_content) == bytes_content

    def test_should_raise_desserialization_error_when_content_is_not_pickle(
        self, pickle_serializer, bytes_content_with_invalid_pickle
    ):
        with pytest.raises(
            DeserializationError, match="Failed to deserialize data"
        ):
            pickle_serializer.loads(bytes_content_with_invalid_pickle)

    def test_should_raise_serialization_error_when_content_is_not_pickle(
        self, pickle_serializer, dict_not_serializable
    ):
        with pytest.raises(
            SerializationError, match="Failed to serialize data"
        ):
            # sets are not pickle serializable
            pickle_serializer.dumps(dict_not_serializable)


class TestJSONSerializer:
    @pytest.fixture
    def json_serializer(self):
        return JSONSerializer()

    @pytest.fixture
    def bytes_content(self):
        return b'{"key": "value"}\x00'

    @pytest.fixture
    def dict_content(self):
        return {"key": "value"}

    @pytest.fixture
    def dict_not_serializable(self):
        return {"key": {1, 2, 3}}

    @pytest.fixture
    def bytes_content_with_invalid_json(self):
        return b'not json'

    def test_loads_should_transform_bytes_into_dict(
        self, json_serializer, bytes_content, dict_content
    ):
        assert json_serializer.loads(bytes_content) == dict_content

    def test_dumps_should_transform_dict_into_bytes(
        self, json_serializer, bytes_content, dict_content
    ):
        assert json_serializer.dumps(dict_content) == bytes_content

    def test_should_raise_desserialization_error_when_content_is_not_json(
        self, json_serializer, bytes_content_with_invalid_json
    ):
        with pytest.raises(
            DeserializationError, match="Failed to deserialize data"
        ):
            json_serializer.loads(bytes_content_with_invalid_json)

    def test_should_raise_serialization_error_when_content_is_not_json(
        self, json_serializer, dict_not_serializable
    ):
        with pytest.raises(
            SerializationError, match="Failed to serialize data"
        ):
            # sets are not json serializable
            json_serializer.dumps(dict_not_serializable)
