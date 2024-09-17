"""Testing App"""

from flask import Flask
from flask.testing import FlaskClient


class TestApp:
    """Test App"""

    def test_app_index(self, client: FlaskClient, APP: Flask):
        """ "Test Main Ingress Point."""

        response = client.get("/")
        assert response is not None
