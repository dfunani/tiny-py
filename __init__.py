"""App Ingress Point."""

import logging
from flask import Flask

logging.basicConfig(
    level=logging.INFO, format="{name}: {levelname} - {message}", style="{"
)
app = Flask(__name__)
