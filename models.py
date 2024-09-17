""""App Data Structures (Models)"""

import os
import random
import string
import logging
from typing import Self
from tinydb import Query, TinyDB
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class URLManagerError(Exception):
    """ "Custom Exceptions."""


class Document(BaseModel):
    """Data Class for Document Loaded to Storage."""

    url: str
    base: str
    key: str


class Storage:
    """ "Singleton Storage Manager."""

    __INSTANCE = None
    __DB_NAME = "tinydb.json"

    def __new__(cls, filename: str = __DB_NAME) -> Self:
        """Ensures Only one Instance of the Storage Class.
        Inits DB on a New Singleton instance."""

        if not cls.__INSTANCE:
            cls.__DB_NAME = filename
            cls.__db = TinyDB(f"{os.path.realpath('storage')}/{cls.__DB_NAME}", indent=4)
            cls.__INSTANCE = super(Storage, cls).__new__(cls)
        return cls.__INSTANCE

    def write(self, document: Document) -> str:
        """Writes to the Storage DB."""

        response = self.__db.insert(document.model_dump())
        return f"Document ID {response} Inserted"

    def read(self, field: str, value: str) -> Document:
        """Reads from the Storage DB - Based on the Field Value Pair provided."""
        query = Query()
        response = self.__db.search(query[field] == value)
        if len(response) != 1:
            return Document(url="", base="", key="")
        return Document(**response[0])

    def exists(self, field: str, value: str) -> bool:
        """Checks if a Field Value Pair exists in the DB."""

        query = Query()
        return self.__db.contains(query[field] == value)


class URLManager:
    """Abstraction of the Mapping of the URL to Token Key and the its persistance."""

    __CHARACTERS = list(string.ascii_lowercase + "0123456789")
    __KEY_LENGTH = 6

    def __init__(self, base_url) -> None:
        self.__base_url = base_url

    def encode(self, url) -> str:
        """Returns a Tokenized URL."""

        if Storage().exists("url", url):
            response = Storage().read("url", url)
            return f"{response.base}{response.key}"
        key = self.generate_url_key()
        encoded_url = f"{self.__base_url}{self.generate_url_key()}"
        try:
            Storage().write(Document(url=url, base=self.__base_url, key=key))
        except ValueError as error:
            logger.critical("Encoder: %s", error)
            raise URLManagerError("Invalid Document.") from error
        return encoded_url

    def decode(self, key: str) -> str:
        """Returns the URL mapped to the Token Key."""
        response = Storage().read("key", key)
        url = response.url
        if not url:
            logger.critical("Decoder: %s", response)
            raise URLManagerError("Invalid Key.")
        return url

    def generate_url_key(self) -> str:
        """Generates a Token Key."""

        key = "".join(self.__CHARACTERS[0 : self.__KEY_LENGTH + 1])
        while Storage().exists("key", key):
            random.shuffle(self.__CHARACTERS)
            key = "".join(self.__CHARACTERS[0 : self.__KEY_LENGTH + 1])
        return key
