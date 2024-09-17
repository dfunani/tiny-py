"""Test Config"""

import os
from flask import Flask
from pytest import fixture

from ..models import Storage
from .. import app


@fixture()
def APP():
    app.config.update({"TESTING": True})
    app.config['SERVER_NAME'] = 'localhost:5000'  # Replace with your actual server name and port
    app.config['APPLICATION_ROOT'] = '/'  # Set the root path if needed
    app.config['PREFERRED_URL_SCHEME'] = 'https'  # Use 'https' for production, 'http' for development

    yield app


@fixture()
def client(APP: Flask):
    return APP.test_client()


@fixture()
def runner(APP: Flask):
    return APP.test_cli_runner()


@fixture()
def document():
    """ "Test Document"""

    return {
        "url": "http://mock-url.com/",
        "base": "http://localhost:8000/",
        "key": "abcdefg",
    }


@fixture()
def storage():
    """Test Storage"""

    filename = "test.json"
    yield Storage(filename)
    try:
        os.remove(f"{os.path.realpath('storage')}/{filename}")
    except FileNotFoundError:
        pass
