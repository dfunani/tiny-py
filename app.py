import logging
import os
from flask import Flask, Response, request, redirect, render_template

from models import URLManager, URLManagerError

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def encode():
    json_request = False
    if request.is_json:
        body = request.get_json()
        json_request = True
    elif request.form:
        body = request.form
    else:
        return Response("Invalid Request Body: Content-Type", status=400)
    
    if "url" not in body:
        return Response("Invalid Request Body: No URL.", status=400)
    
    try:
        url = body["url"]
        response = URLManager(request.url_root).encode(url)
        if json_request:
            return Response(response, status=200)
        return render_template("view.html", url=response)
    except URLManagerError as error:
        return str(error)


@app.route(f"/<string:key>")
def decode(key):
    try:
        url = URLManager(request.root_url).decode(key)
    except URLManagerError as error:
        return str(error)
    return redirect(url, code=302)
