"""Testing Models"""

# mypy: disable_error_code="arg-type"

from pydantic import BaseModel, ValidationError
from pytest import raises

from ..models import Document, Storage, URLManagerError


class TestModels:
    """Test Models"""

    def test_url_manager_error(self):
        """ "Test Custom Exception."""

        with raises(URLManagerError, match="Invalid Document."):
            raise URLManagerError("Invalid Document.")

    def test_document_data_class(self, document: dict):
        """ "Test Custom Data Class."""

        response = Document(**document)
        assert isinstance(response, BaseModel)
        for key, value in response.model_dump().items():
            assert isinstance(value, type(document[key]))

    def test_invalid_document_data_class(self, document: dict):
        """ "Test Invalid Custom Data Class."""

        document.update({"key": 1})
        with raises(ValidationError):
            Document(**document)

    def test_storage_write(self, document: dict, storage: Storage):
        """ "Test Storage Writer."""

        assert storage.write(Document(**document)) == "Document ID 1 Inserted"

    def test_storage_write_null(self, storage: Storage):
        """ "Test Storage Writer."""

        with raises(AttributeError):
            storage.write("")

    def test_storage_read(self, document: dict, storage: Storage):
        """ "Test Storage Reader."""

        doc = storage.read("key", document["key"])
        assert isinstance(doc, BaseModel)
        for key, value in doc.model_dump().items():
            assert value == document[key]

    def test_storage_read_null(self, storage: Storage):
        """ "Test Custom Exception"""

        doc = storage.read("key", "test")
        assert isinstance(doc, BaseModel)
        for _, value in doc.model_dump().items():
            assert value == ""

    def test_storage_exists(self, document: dict, storage: Storage):
        """ "Test Existence"""

        assert storage.exists("key", document["key"])

    def test_storage_does_not_exist_value(self, storage: Storage):
        """ "Test Non-Existence"""

        assert not storage.exists("key", "test")

    def test_storage_does_not_exist_key(self, storage: Storage):
        """ "Test Non-Existence - Invalid Field"""

        assert not storage.exists("keys", "test")
