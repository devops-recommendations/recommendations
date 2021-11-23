"""
RECOMMENDATIONS SERVICE

Paths:
------
GET / - Root Resource
GET /recommendations - Return a list of all recommendations for all products
POST /recommendation - Add a recommendation for products
"""
from flask import request, abort
from flask_restx import Api, Resource, fields
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from service.models import Recommendation
# Import Flask application
from . import app, status


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    return app.send_static_file('index.html')


# ######################################################################
# # Configure Swagger before initializing it
# ######################################################################
api = Api(
    app,
    version='1.0.0',
    title='Recommendations REST API Service',
    description='This is a sample server for the recommendation service.',
    default='recommendation',
    default_label='Recommendation Management',
    doc='/apidocs'
)

# Model definition starts
create_recommendation_model = api.model(
    'CreateRecommendationModel', {
        'product_id': fields.Integer(required=True,
                                     description='The name of the Recommendation'),
        'rec_product_id': fields.Integer(required=True,
                                         description='ID of the recommended product'),
        'type': fields.String(required=True,
                              description='Type of the recommendation (Generic, BoughtTogether, CrossSell, UpSell, '
                                          'Complementary)'),
        'interested': fields.Integer(required=False,
                                     description='Interested counter for each recommendation')
    })

recommendation_model = api.inherit(
    'RecommendationModel',
    create_recommendation_model,
    {'id': fields.Integer(readOnly=True,
                          decription="The unique id assigned internally by service")}
)


# Model definition ends

######################################################################
#  PATH: /recommendations/{id}
######################################################################
@api.route('/recommendations/<int:id>')
@api.param('id', 'Recommendation identifier')
class RecommendationResource(Resource):
    """
    RecommendationResource class
    Allows the manipulation of a single Recommendation
    GET /{id} - Returns a recommendation with the id
    PUT /{id} - Update a recommendation with the id
    DELETE /{id} -  Deletes a recommendation with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A Recommendation
    # ------------------------------------------------------------------
    @api.response(404, 'Recommendation not found')
    @api.marshal_with(recommendation_model)
    def get(self, id):
        """
        Retrieve a single recommendation
        This endpoint will return a recommendation based on it's id
        """
        app.logger.info("Request to Retrieve a recommendation with id [%s]", id)
        recommendation = Recommendation.find(id)
        if not recommendation:
            abort(status.HTTP_404_NOT_FOUND, "Recommndation with id '{}' was not found.".format(id))
        app.logger.info("Returning recommendation: %s", recommendation.id)
        return recommendation.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING Recommendation
    # ------------------------------------------------------------------
    @api.response(404, 'Recommendation not found')
    @api.response(400, 'The posted recommndation data was not valid')
    @api.expect(create_recommendation_model)
    @api.marshal_with(create_recommendation_model)
    def put(self, id):
        """
        Update a recommendation
        This endpoint will update a recommendation based the body that is posted
        """
        app.logger.info('Request to Update a recommendation with id [%s]', id)
        recommendation = Recommendation.find(id)
        if not recommendation:
            abort(status.HTTP_404_NOT_FOUND, "Recommendation with id '{}' was not found.".format(id))
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        recommendation.deserialize(data)
        recommendation.id = id
        recommendation.update()
        return recommendation.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A RECOMMENDATION
    # ------------------------------------------------------------------
    @api.response(204, 'Recommendation deleted')
    def delete(self, id):
        """
        Delete a Recommendation
        This endpoint will delete a Recommendation based the id specified in the path
        """
        app.logger.info('Request to Delete a recommendation with id [%s]', id)
        recommendation = Recommendation.find(id)
        if recommendation:
            recommendation.delete()
            app.logger.info('Recommendation with id [%s] was deleted', id)

        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /recommendations
######################################################################
@api.route('/recommendations', strict_slashes=False)
class RecommendationCollection(Resource):
    """ Handles all interactions with collections of Recommendations """

    # ------------------------------------------------------------------
    # LIST ALL RECOMMENDATION
    # ------------------------------------------------------------------
    @api.marshal_list_with(recommendation_model)
    def get(self):
        """ Returns all of the Recommendations """
        app.logger.info('Request to list Recommendations...')
        recommendations = []
        product_id = request.args.get('product_id')
        rec_product_id = request.args.get("rec_product_id")
        rec_type = request.args.get("type")

        if product_id or rec_product_id or rec_type:
            recommendations = Recommendation.find_rec_by_filter(
                product_id=product_id,
                rec_product_id=rec_product_id,
                type=rec_type
            )
        else:
            recommendations = Recommendation.all()

        results = [recommendation.serialize()
                   for recommendation in recommendations]
        app.logger.info("Returning %d recommendations", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW RECOMMENDATION
    # ------------------------------------------------------------------
    @api.expect(create_recommendation_model)
    @api.response(400, 'The posted data was not valid')
    @api.marshal_with(create_recommendation_model, code=201)
    def post(self):
        """
        Creates a Recommendation
        This endpoint will create a Recommendation based the data in the body that is posted
        """
        app.logger.info('Request to Create a Recommendation')
        check_content_type("application/json")
        recommendation = Recommendation()
        app.logger.debug('Payload = %s', api.payload)
        recommendation.deserialize(api.payload)
        recommendation.create()
        app.logger.info('Recommendation with new id [%s] created!', recommendation.id)
        location_url = api.url_for(RecommendationResource, id=recommendation.id, _external=True)
        return recommendation.serialize(), status.HTTP_201_CREATED, {'Location': location_url}

    # ------------------------------------------------------------------
    # DELETE ALL RECOMMENDATIONS (for testing only)
    # ------------------------------------------------------------------
    @api.response(204, 'All Recommendations deleted')
    def delete(self):
        """
        Delete all Recommendation
        This endpoint will delete all Recommendation only if the system is under test
        """
        app.logger.info('Request to Delete all recommendations...')
        if "TESTING" in app.config and app.config["TESTING"]:
            Recommendation.remove_all()
            app.logger.info("Removed all Recommendations from the database")
        else:
            app.logger.warning("Request to clear database while system not under test")

        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /recommendations/{id}/interested
######################################################################
@api.route('/recommendations/<id>/interested')
@api.param('id', 'The Recommendation identifier')
class InterestedResource(Resource):
    """ Action on a Recommendation """

    @api.response(404, 'Recommendation not found')
    @api.response(409, 'The Recommendation is not available to increment interested')
    def put(self, id):
        """
        Increment a recommendation's interesed field
        This endpoint will increment the interested counter by one when interested button is clicked
        """
        app.logger.info(
            'Increment intrested field for recommendation with id: %s', id)
        check_content_type('application/json')
        recommendation = Recommendation.find(id)
        if not recommendation:
            raise NotFound(
                "Recommendation with id '{}' was not found.".format(id))
        recommendation.interested += 1
        recommendation.update()

        app.logger.info(
            "Interested count with recommendation ID [%s] updated.", recommendation.id)
        return recommendation.serialize(), status.HTTP_200_OK


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
