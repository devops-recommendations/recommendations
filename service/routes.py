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


# GET INDEX
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Recommendations REST API Service",
            version="0.1",
        ),
        status.HTTP_200_OK,
    )
