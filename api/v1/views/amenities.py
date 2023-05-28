#!/usr/bin/python3
""" Configures RESTful api for the amenities route """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def appViewAllAmenities():
    """ Amenities api route """

    if request.method == "GET":
        amObjs = storage.all(Amenity)
        amList = []
        for amenity in amObjs.values():
            amList.append(amenity.to_dict())

        return jsonify(amList)
    else:
        try:
            jsonDict = request.get_json()
            if not jsonDict:
                raise TypeError("Not a JSON")
        except Exception:
            abort(400, "Not a JSON")

        try:
            name = jsonDict[name]
        except KeyError:
            abort(400, "Missing name")

        newAm = Amenity(**jsonDict)
        storage.new(newAm)
        storage.save()
        return jsonify(newAm.to_dict()), 201


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False)
def appViewAmenity(amenity_id):
    """ configures the amenities/<amenity_id> route """

    am = storage.get("Amenity", amenity_id)

    if not am:
        abort(404)

    if request.method == "GET":
        return jsonify(am.to_dict())
    elif request.method == "DELETE":
        storage.delete(am)
        storage.save()
        return jsonify({}), 200
    else:
        try:
            jsonDict = request.get_json()
            if not jsonDict:
                raise TypeError("Not a JSON")
        except Exception:
            abort(400, "Not a JSON")

    ignore = ["id", "created_at", "updated_at"]
    for key, val in jsonDict.items():
        if key not in ignore:
            setattr(am, key, val)
    storage.save()
    return jsonify(am.to_dict()), 200
