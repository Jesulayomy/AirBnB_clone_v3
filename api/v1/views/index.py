#!/usr/bin/python3
""" sets the status app route """
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
        }


@app_views.route('/stats', strict_slashes=False)
def appViewStats():
    """ returns the json stats of the count of all states """

    counts = {}
    for cls_name, cls_obj in classes.items():
        counts[cls_name] = storage.count(cls_obj)
    return jsonify(counts)


@app_views.route('/status', strict_slashes=False)
def appViewStatus():
    """ returns the json status: ok """

    dct = {"status": "OK"}
    return jsonify(dct)
