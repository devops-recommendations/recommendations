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
    return (jsonify(), status.HTTP_200_OK)

@app.route("/recommendations/<int:prod_id>", methods=["GET"])
def list_recommendations(prod_id):
    """Returns all of recommendations for a product"""
    app.logger.info("Request for recommendations for product with id: %s", prod_id)
    product = Product.find(prod_id)
    if not product:
        raise NotFound("Product with id '{}' was not found.".format(prod_id))

    app.logger.info("Returning recommendations for product: %s", product.name)
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)
    