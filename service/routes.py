"""
RECOMMENDATIONS SERVICE

Paths:
------
GET / - Root Resource
GET /recommendations - Return a list of all recommendations for all products
POST /recommendation - Add a recommendation for products
"""
import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Recommendation, DataValidationError

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Recommendation REST API Service",
            version="1.0",
            description="The recommendations resource can be used to get a product recommendation based on another product.",
            paths=url_for("list_recommendations", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
# LIST ALL RECOMMENDATIONS
######################################################################


@app.route("/recommendations", methods=["GET"])
def list_recommendations():
    """Returns all of the Recommendations for all products"""

    app.logger.info("Request for recommendations list")
    recommendations = []
    query_prod_id = request.args.get('query_prod_id')

    if query_prod_id:
        recommendations = Recommendation.find_by_query_prod_id(query_prod_id)
    else:
        recommendations = Recommendation.all()

    results = [recommendation.serialize()
               for recommendation in recommendations]
    app.logger.info("Returning %d recommendations", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# CREATE A RECOMMENDATION
######################################################################


@app.route("/recommendations", methods=["POST"])
def create_recommendation():
    """
    Creates a Recommendation
    This endpoint will create a Recommendation based the data in the body that is posted
    """
    app.logger.info("Request to create a recommendation")
    check_content_type("application/json")
    recommendation = Recommendation()
    recommendation.deserialize(request.get_json())
    recommendation.create()
    message = recommendation.serialize()
    location_url = url_for("list_recommendations",
                           rec_id=recommendation.id, _external=True)

    app.logger.info("Recommendation with ID [%s] created.", recommendation.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# RETRIEVE A RECOMMENDATION
######################################################################


@app.route("/recommendations/<int:rec_id>", methods=["GET"])
def get_recommendations(rec_id):
    """
    Retrieve a single Recommendation
    This endpoint will return a Recommendation based on it's id
    """
    app.logger.info("Request for recommendation with id: %s", rec_id)
    recommendation = Recommendation.find(rec_id)
    if not recommendation:
        raise NotFound(
            "Recommendation with id '{}' was not found.".format(rec_id))

    app.logger.info("Returning recommendation: %s", recommendation.id)
    return make_response(jsonify(recommendation.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE A RECOMMENDATION
######################################################################


@app.route("/recommendations/<int:rec_id>", methods=["DELETE"])
def delete_recommendations(rec_id):
    """
    Delete a single Recommendation
    This endpoint will delete a Recommendation based the id specified in the path
    """
    app.logger.info("Request to delete recommendation with id: %s", rec_id)
    recommendation = Recommendation.find(rec_id)
    if recommendation:
        recommendation.delete()

    app.logger.info("Recommendation with ID [%s] delete complete.", rec_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# UPDATE AN EXISTING RECOMMENDATION
######################################################################


@app.route("/recommendations/<int:rec_id>", methods=["PUT"])
def update_recommendations(rec_id):
    """
    Update a Recommendation
    This endpoint will update a Recommendation based the body that is posted
    """
    app.logger.info("Request to update recommendations with id: %s", rec_id)
    check_content_type("application/json")
    recommendation = Recommendation.find(rec_id)
    if not recommendation:
        raise NotFound(
            "Recommendation with id '{}' was not found.".format(rec_id))
    recommendation.deserialize(request.get_json())
    recommendation.id = rec_id
    recommendation.update()

    app.logger.info("Recommendation with ID [%s] updated.", recommendation.id)
    return make_response(jsonify(recommendation.serialize()), status.HTTP_200_OK)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )

######################################################################
#  Increment Interested Counter
######################################################################


@app.route('/recommendations/<int:rec_id>/interested', methods=["PUT"])
def increment_interested_counter(rec_id):
    """
    Increment a recommendation's interesed field
    This endpoint will increment the interested counter by one when interested button is clicked
    """
    app.logger.info(
        'Increment intrested field for recommendation with id: %s', rec_id)
    check_content_type('application/json')
    recommendation = Recommendation.find(rec_id)
    if not recommendation:
        raise NotFound(
            "Recommendation with id '{}' was not found.".format(rec_id))
    recommendation.rec_interested += 1
    recommendation.update()

    app.logger.info(
        "Interested count with recommnedation product ID [%s] updated.", recommendation.rec_prod_id)

    return make_response(jsonify(recommendation.serialize()), status.HTTP_200_OK)
