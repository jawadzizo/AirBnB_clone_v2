#!/usr/bin/python3
"""Starts a Flask web application."""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """prints an HTML page full of all States."""
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """prints an HTML page with cities inside of the state's<id>"""
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown(exc):
    """closes SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
