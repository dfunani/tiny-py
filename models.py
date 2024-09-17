import random
import string
import logging
from typing import Self
from tinydb import Query, TinyDB
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class URLManagerError(Exception):
    pass


class Document(BaseModel):
    url: str
    base: str
    key: str


class Storage:
    __INSTANCE = None
    __DB_NAME = "tinydb.json"

    def __new__(cls) -> Self:
        if not cls.__INSTANCE:
            cls.__db = TinyDB(cls.__DB_NAME)
            cls.__INSTANCE = super(Storage, cls).__new__(cls)
        return cls.__INSTANCE

    def write(self, document: Document) -> str:
        response = self.__db.insert(document.model_dump())
        return f"Document ID {response} Inserted"

    def read(self, field: str, value: str) -> Document:
        query = Query()
        response = self.__db.search(query[field] == value)
        if len(response) != 1:
            return Document(url="", base="", key="")
        return response[0]

    def exists(self, field: str, value: str) -> bool:
        query = Query()
        return self.__db.contains(query[field] == value)


class URLManager:
    __CHARACTERS = list(string.ascii_lowercase + "0123456789")
    __KEY_LENGTH = 6

    def __init__(self, base_url) -> None:
        self.__base_url = base_url

    @property
    def key_length(self) -> int:
        return self.__KEY_LENGTH

    def encode(self, url) -> str:
        if Storage().exists("url", url):
            response = dict(Storage().read("url", url))
            return f"{response['base']}{response['key']}"
        key = self.generate_url_key()
        encoded_url = f"{self.__base_url}{self.generate_url_key()}"
        try:
            Storage().write(Document(url=url, base=self.__base_url, key=key))
        except ValueError as error:
            logger.critical(f"Encoder: {error}")
            raise URLManagerError("Invalid Document.") from error
        return encoded_url

    def decode(self, key: str) -> str:
        response = Storage().read("key", key)
        url = dict(response)["url"]
        if not url:
            logger.critical(f"Decoder: {response}")
            raise URLManagerError("Invalid Key.")
        return url

    def generate_url_key(self) -> str:
        key = "".join(self.__CHARACTERS[0 : self.__KEY_LENGTH + 1])
        while Storage().exists("key", key):
            random.shuffle(self.__CHARACTERS)
            key = "".join(self.__CHARACTERS[0 : self.__KEY_LENGTH + 1])
        return key
