#!/usr/bin/python3
""" Starts the Applicaion with flsak framework """
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def pageNotFound(err):
    """ Throws a json error for a not found page """

    errDct = {"error": "Not found"}
    return jsonify(errDct), 404


@app.teardown_appcontext
def shutDown(exception):
    """ Shuts down the flask app """

    storage.close()


if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST", default='0.0.0.0'),
            port=os.getenv("HBNB_API_PORT", default=5000),
            threaded=True
            )
