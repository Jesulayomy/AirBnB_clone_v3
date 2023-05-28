#!/usr/bin/python3
""" calls to the state route """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def appViewAllStates():
    """ returns the json rerpresentation of the state object """

    if request.method == 'GET':
        dct = storage.all(State)
        statesList = []
        for obj in dct.values():
            statesList.append(obj.to_dict())
        return jsonify(statesList)
    else:
        try:
            statesDict = request.get_json()
            if not statesDict:
                raise TypeError("Err")
        except Exception:
            abort(400, "Not a JSON")

        try:
            stateName = statesDict['name']
        except KeyError:
            abort(400, "Missing name")

        newState = State(**statesDict)
        storage.new(newState)
        storage.save()

        return jsonify(newState.to_dict()), 201


@app_views.route(
        '/states/<state_id>',
        methods=['DELETE', 'GET', 'PUT'],
        strict_slashes=False)
def appViewStates(state_id=None):
    """ returns the json rerpresentation of the state object """

    stateObj = storage.get(State, state_id)
    if not stateObj:
        abort(404)

    if request.method == "GET":
        return jsonify(stateObj.to_dict())
    elif request.method == "DELETE":
        storage.delete(stateObj)
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
        stateDict = stateObj.to_dict()
        for key, value in jsonDict.items():
            if key not in ignore and key in stateDict:
                setattr(stateObj, key, value)

        storage.save()
        return jsonify(stateObj.to_dict()), 200
