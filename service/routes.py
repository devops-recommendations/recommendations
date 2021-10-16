"""
RECOMMENDATIONS SERVICE

Paths:
------
GET / - Root Resource
"""

from flask import jsonify

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
            paths=[url_for("list_recommendations", _external=True)],
        ),
        status.HTTP_200_OK,
    )
