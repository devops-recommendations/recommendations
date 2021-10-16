"""
RECOMMENDATIONS SERVICE

Paths:
------
GET / - Root Resource
GET /recommendations - Return a list of all recommendations for all products
"""

from flask import Flask, jsonify, request, url_for, make_response, abort

from service.models import Recommendation
from werkzeug.exceptions import NotFound
# Import Flask application
from . import app
from . import status  # HTTP Status Codes


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
    recommendations = Recommendation.all()

    results = [recommendation.serialize()
               for recommendation in recommendations]
    app.logger.info("Returning %d recommendations", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)
