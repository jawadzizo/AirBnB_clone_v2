#!/usr/bin/python3
"""Starts a flask application."""
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """prints 'Hello HBNB!'"""
    return "Hello HBNB!"
