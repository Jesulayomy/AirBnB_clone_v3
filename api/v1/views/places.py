#!/usr/bin/python3
""" Configures RESTful api for the places route """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place


@app_views.route(
        "cities/<city_id>/places",
        methods=["GET", "POST"],
        strict_slashes=False)
def appViewPlaces(city_id):
    """ configures the places route through the cities repationship """

    city = storage.get("City", city_id)
    if not city:
        abort(404)

    if request.method == "GET":
        placesDict = []
        for place in city.places:
            placesDict.append(place.to_dict())

        return jsonify(placesDict)
    else:
        try:
            jsonDict = request.get_json()
            if not jsonDict:
                raise TypeError("Not a JSON")
        except Exception:
            abort(400, "Not a JSON")

        try:
            user_id = jsonDict["user_id"]
        except KeyError:
            abort(400, "Missing user_id")

        user = storage.get("User", user_id)
        if not user:
            abort(404)
        try:
            name = jsonDict["name"]
        except KeyError:
            abort(400, "Missing name")

        new_place = Place(**jsonDict)
        new_place.city_id = city_id
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route(
        "/places/<place_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False)
def appViewPlacesID(place_id):
    """ configures the places/<place_id> route to retrieve a specfic place """

    place = storage.get("Place", place_id)

    if not place:
        abort(404)

    if request.method == "GET":
        return jsonify(place.to_dict())
    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        try:
            jsonDict = request.get_json()
            if not jsonDict:
                raise TypeError("Not a JSON")
        except Exception:
            abort(400, "Not a JSON")
        ignore = [
                "id", "user_id", "city_id",
                "created_at", "updated_at"
                ]
        for key, val in jsonDict.items():
            if key not in ignore:
                setattr(place, key, val)

        storage.save()
        return jsonify(place.to_dict()), 200


@app_views.route(
        "/places_search",
        methods=["POST"],
        strict_slashes=False)
def appViewPlacesSearch():
    """ configures route for places_search """

    try:
        jsonDict = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    places = storage.all(Place)
    places_dict = [place.to_dict() for place in places.values()]

    if not jsonDict:
        return jsonify(places_dict)

    if not jsonDict.get("states") and (
            not jsonDict.get("cities")) and (
            not jsonDict.get("amenities")):
        return jsonify(places_dict)

    result = []

    if jsonDict.get("states"):
        for state_id in jsonDict["states"]:
            state = storage.get("State", state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        if place not in result:
                            result.append(place)

    if jsonDict.get("cities"):
        for city_id in jsonDict["cities"]:
            city = storage.get("City", city_id)
            if city:
                for place in city.places:
                    if place not in result:
                        result.append(place)

    if jsonDict.get("amenities"):
        if not result:
            result = [place for place in places.values()]
        filt = []
        amenities = []
        for amenity_id in jsonDict["amenities"]:
            amenities.append(storage.get("Amenity", amenity_id))

        for place in result:
            place_amenities = place.amenities
            has_all = True
            for amenity in amenities:
                if amenity not in place_amenities:
                    has_all = False
                    break

            if has_all:
                filt.append(place)
        for place in filt:
            place_dict = place.to_dict()
            if "amenities" in place_dict:
                del place_dict["amenities"]
            filt_dict.append(place_dict)

        return jsonify(filt_dict)

    result_dict = [place.to_dict() for place in result]
    return jsonify(result_dict)
    """ configures route for places_search """
