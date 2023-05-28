#!/usr/bin/python3
""" this module configures RESTful api for the places_amenities route """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
import os


@app_views.route(
        "places/<place_id>/amenities",
        methods=["GET"],
        strict_slashes=False)
def appViewPlacesAmenities(place_id):
    """ displacys amenities by places configures the places_amenities route """

    pl = storage.get("Place", place_id)
    if not pl:
        abort(404)

    places_amenities = pl.amenities
    amenitiesList = []
    for amenity in places_amenities:
        amenitiesList.append(amenity.to_dict())
    return jsonify(amenitiesList)


@app_views.route(
        "places/<place_id>/amenities/<amenity_id>",
        methods=["DELETE", "POST"],
        strict_slashes=False)
def appViewPlacesAmenitiesID(place_id, amenity_id):
    """ configures the places/<place_id>/amenities/ route """

    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    storage_type = os.getenv("HBNB_TYPE_STORAGE")

    if not amenity or not place:
        abort(404)

    if request.method == "DELETE":
        if amenity not in place.amenities:
            abort(404)

        if storage_type == "db":
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.remove(amenity_id)

        storage.save()

        return jsonify({}), 200
    else:
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        if storage_type == "db":
            place.amenities.append(amenity)
        else:
            place.amenity_ids.append(amenity_id)

        storage.save()
        return jsonify(amenity.to_dict()), 201
