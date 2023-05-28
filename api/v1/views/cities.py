#!/usr/bin/python3
""" calls to the city route """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route(
        '/states/<state_id>/cities',
        methods=['GET', 'POST'],
        strict_slashes=False)
def appViewAllCity(state_id):
    """
        returns the json rerpresentation of the city
        objects linked to <state_id>
    """
    stateObj = storage.get("State", state_id)

    if request.method == 'GET':
        citiesList = []
        for city in stateObj.cities:
            citiesList.append(city.to_dict())
        return jsonify(citiesList)
    else:
        try:
            citiesDict = request.get_json()
            if not citiesDict:
                raise TypeError("Err")
        except Exception:
            abort(400, "Not a JSON")

        try:
            cityName = citiesDict['name']
        except KeyError:
            abort(400, "Missing name")

        newCity = City(**citiesDict)
        storage.new(newCity)
        storage.save()

        return jsonify(newCity.to_dict()), 201


@app_views.route(
        '/cities/<city_id>',
        methods=['DELETE', 'GET', 'PUT'],
        strict_slashes=False)
def appViewCity(city_id):
    """ returns the json rerpresentation of the city object """

    cityObj = storage.get("City", city_id)
    if not cityObj:
        abort(404)

    if request.method == "GET":
        return jsonify(cityObj.to_dict())
    elif request.method == "DELETE":
        storage.delete(cityObj)
        storage.save()
        return jsonify({}), 200
    else:
        try:
            jsonDict = request.get_json()
            if not jsonDict:
                raise TypeError("Err")
        except Exception:
            abort(400, "Not a JSON")

        ignore = ["id", "created_at", "updated_at"]
        cityDict = cityObj.to_dict()
        for key, value in jsonDict.items():
            if key not in ignore:
                setattr(cityObj, key, value)

        storage.save()
        return jsonify(cityObj.to_dict()), 200
