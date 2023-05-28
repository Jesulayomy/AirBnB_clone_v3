#!/usr/bin/python3
""" Users route rest api """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def appViewUsers():
    """ configures the user route get and post requests """

    if request.method == "GET":
        users = storage.all(User)
        usersList = []
        for user in users.values():
            usersList.append(user.to_dict())
        return jsonify(usersList)
    else:
        try:
            jsonDict = request.get_json()
            if not jsonDict:
                raise TypeError("Not a JSON")
        except Exception:
            abort(400, "Not a JSON")

        try:
            email = json_dict["email"]
        except KeyError:
            abort(400, "Missing email")
        try:
            password = json_dict["password"]
        except KeyError:
            abort(400, "Missing password")

        newUser = User(**jsonDict)
        storage.new(newUser)
        storage.save()
        return jsonify(newUser.to_dict()), 201


@app_views.route(
        "/users/<user_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False)
def appViewUser(user_id):
    """ returns a single user for the users/<user_id> route """

    userObj = storage.get("User", user_id)

    if not userObj:
        abort(404)

    if request.method == "GET":
        return jsonify(userObj.to_dict())
    elif request.method == "DELETE":
        storage.delete(userObj)
        storage.save()
        return jsonify({}), 200
    else:
        try:
            jsonDict = request.get_json()
            if not jsonDict:
                raise TypeError("Not a JSON")
        except Exception:
            abort(400, "Not a JSON")

        ignore = ["id", "email", "created_at", "updated_at"]
        for key, val in jsonDict.items():
            if key not in ignore:
                setattr(user, key, val)

        storage.save()
        return jsonify(userObj.to_dict()), 200
