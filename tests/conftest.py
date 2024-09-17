"""Test Config"""

import os
from pytest import fixture

from ..models import Storage


@fixture
def document():
    """ "Test Document"""

    return {
        "url": "http://mock-url.com/",
        "base": "http://localhost:8000/",
        "key": "abcdefg",
    }


@fixture
def storage():
    """Test Storage"""

    filename = "test.json"
    yield Storage(filename)
    try:
        os.remove(f"{os.path.realpath('storage')}/{filename}")
    except FileNotFoundError:
        pass
