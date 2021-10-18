"""
TestYourResourceModel API Service Test Suite
Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import unittest
from unittest import mock

from urllib.parse import quote_plus
from service import status  # HTTP Status Codes
from service.models import db, init_db, DataValidationError
from service.routes import app
from .factories import RecommendationFactory

# Disable all but ciritcal errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/recommendations"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(unittest.TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_recommendations(self, count):
        """Factory method to create recommendations in bulk"""

        recommendations = []
        for _ in range(count):
            test_recommendation = RecommendationFactory()
            resp = self.app.post(
                BASE_URL, json=test_recommendation.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test recommendation"
            )
            new_recommendation = resp.get_json()
            test_recommendation.id = new_recommendation["id"]
            recommendations.append(test_recommendation)

        return recommendations

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Recommendation REST API Service")

    def test_get_recommendations_list(self):
        """Get a list of Recommendations"""
        self._create_recommendations(5)
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_create_recommendation(self):
        """Create a new Recommendation"""
        test_rec = RecommendationFactory()
        logging.debug(test_rec)
        resp = self.app.post(
            BASE_URL, json=test_rec.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_rec = resp.get_json()
        self.assertEqual(
            new_rec["query_prod_id"], test_rec.query_prod_id, "Query_prod_id do not match")
        self.assertEqual(
            new_rec["rec_prod_id"], test_rec.rec_prod_id, "Rec_prod do not match"
        )
        self.assertEqual(
            new_rec["type"], test_rec.type.name, "Type does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_rec = resp.get_json()
        self.assertEqual(new_rec[0]['query_prod_id'],
                         test_rec.query_prod_id, "Query_prod_id do not match")
        self.assertEqual(
            new_rec[0]["rec_prod_id"], test_rec.rec_prod_id, "Rec_prod do not match"
        )
        self.assertEqual(
            new_rec[0]["type"], test_rec.type.name, "Type does not match"
        )

    def test_get_recommendation(self):
        """Get a single recommendation"""
        # get the id of a recommendation
        test_rec = self._create_recommendations(1)[0]
        resp = self.app.get(
            "/recommendations/{}".format(test_rec.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["query_prod_id"], test_rec.query_prod_id)

    def test_get_recommendation_not_found(self):
        """Get a Recommendation thats not found"""
        resp = self.app.get("/recommendations/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_recommendation(self):
        """Delete a Recommendation"""
        test_recommendation = self._create_recommendations(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_recommendation.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_recommendation.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_recommendation(self):
        """Update an existing Recommendation"""
        # create a recommendation to update
        test_recommendation = RecommendationFactory()
        resp = self.app.post(
            BASE_URL, json=test_recommendation.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the recommendation
        new_recommendation = resp.get_json()
        logging.debug(new_recommendation)
        new_recommendation["query_prod_id"] = 5
        resp = self.app.put(
            "/recommendations/{}".format(new_recommendation["id"]),
            json=new_recommendation,
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_recommendation = resp.get_json()
        self.assertEqual(updated_recommendation["query_prod_id"], 5)

    def test_create_recommendation_bad_type(self):
        """ Create a recommendation with bad type data """
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        # change type to a bad string
        test_recommendation = recommendation.serialize()
        test_recommendation["type"] = "no_such_type"    # wrong type
        resp = self.app.post(
            BASE_URL, json=test_recommendation, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recommendation_no_content_type(self):
        """Create a recommendation with no content type"""
        resp = self.app.post(BASE_URL)
        self.assertEqual(resp.status_code,
                         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
