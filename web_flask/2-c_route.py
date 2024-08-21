#!/usr/bin/python3
"""Starts a flask application."""
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """prints 'Hello HBNB!'"""
    return "Hello HBNB!"

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """prints 'HBNB'."""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """prints 'C' followed by the value of <text>."""
    text = text.replace("_", " ")
    return f"C {text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
