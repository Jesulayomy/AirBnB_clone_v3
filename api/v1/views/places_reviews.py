#!/usr/bin/python3
""" Configures RESTful api for the reviews route """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review


@app_views.route(
        "places/<place_id>/reviews",
        methods=["GET", "POST"],
        strict_slashes=False)
def appViewReviews(place_id):
    """ configures the reviews route to display the json representation """

    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if request.method == "GET":
        reviewsList = []
        for review in place.reviews:
            reviewsList.append(review.to_dict())

        return jsonify(reviewsList)
    else:
        try:
            jsonDict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        if not jsonDict:
            abort(400, "Not a JSON")

        try:
            user_id = jsonDict["user_id"]
        except KeyError:
            abort(400, "Missing user_id")

        user = storage.get("User", user_id)
        if not user:
            abort(404)
        try:
            text = jsonDict["text"]
        except KeyError:
            abort(400, "Missing text")

        new_review = Review(**jsonDict)
        new_review.place_id = place_id
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False)
def appViewReviewsID(review_id):
    """ displays the revies with the given id /reviews/<review_id> route """

    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    if request.method == "GET":
        return jsonify(review.to_dict())
    elif request.method == "DELETE":
        storage.delete(review)
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
                "id", "user_id", "place_id",
                "created_at", "updated_at"
        ]
        for key, val in jsonDict.items():
            if key not in ignore:
                setattr(review, key, val)

        storage.save()
        return jsonify(review.to_dict()), 200
