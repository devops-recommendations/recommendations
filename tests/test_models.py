"""
Test cases for Recommendation Model
Test cases can be run with:
    nosetests
    coverage report -m
While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_models.py:TestRecommendationModel
"""
import os
import logging
from types import resolve_bases
import unittest
from werkzeug.exceptions import NotFound
from service.models import Recommendation, RecommendationType, DataValidationError, db
from service import app
from .factories import RecommendationFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  R E C O M M E N D A T I O N   M O D E L   T E S T   C A S E S
######################################################################


class TestRecommendationModel(unittest.TestCase):
    """Test Cases for Recommendation Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Recommendation.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_recommendation(self):
        """Create a recommendation and assert that it exists"""
        rec = Recommendation(product_id=0, rec_product_id=1,
                             type=RecommendationType.Generic)
        self.assertTrue(rec != None)
        self.assertEqual(rec.id, None)
        self.assertEqual(rec.product_id, 0)
        self.assertEqual(rec.rec_product_id, 1)
        self.assertEqual(rec.type, RecommendationType.Generic)

        rec = Recommendation(product_id=1, rec_product_id=5,
                             type=RecommendationType.UpSell)
        self.assertEqual(rec.product_id, 1)
        self.assertEqual(rec.rec_product_id, 5)
        self.assertEqual(rec.type, RecommendationType.UpSell)

    def test_add_a_recommendation(self):
        """Create a recommendation and add it to the database"""
        recs = Recommendation.all()
        self.assertEqual(recs, [])
        rec = Recommendation(product_id=1, rec_product_id=5,
                             type=RecommendationType.UpSell)
        self.assertTrue(rec != None)
        self.assertEqual(rec.id, None)
        rec.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(rec.id, 1)
        recs = Recommendation.all()
        self.assertEqual(len(recs), 1)

    def test_update_a_recommendation(self):
        """Update a Recommendation"""
        rec = RecommendationFactory()
        logging.debug(rec)
        rec.create()
        logging.debug(rec)
        self.assertEqual(rec.id, 1)
        # Change it an save it
        rec.rec_product_id = 201
        original_id = rec.id
        rec.update()
        self.assertEqual(rec.id, original_id)
        self.assertEqual(rec.rec_product_id, 201)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        recs = Recommendation.all()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0].id, 1)
        self.assertEqual(recs[0].rec_product_id, 201)

    def test_bad_update(self):
        """Test error on invalid update"""
        rec = RecommendationFactory()
        logging.debug(rec)
        rec.create()
        self.assertEqual(rec.id, 1)
        rec.id = None
        self.assertRaises(DataValidationError, rec.update)

    def test_result_string_conversion(self):
        """Test printable representation of Recommendation Model"""
        out = repr(Recommendation(product_id=1, rec_product_id=2,
                   type=RecommendationType.UpSell))
        self.assertEqual(
            out, "<Recommendation of prod=[1] is prod=[2] with id=[None] in table>")

    def test_delete_a_recommendation(self):
        """Delete a Recommendation"""
        rec = RecommendationFactory()
        rec.create()
        self.assertEqual(len(Recommendation.all()), 1)

        rec.delete()
        self.assertEqual(len(Recommendation.all()), 0)

    def test_serialize_a_recommendation(self):
        """Test serialization of a Recommendation"""
        rec = RecommendationFactory()
        data = rec.serialize()
        self.assertNotEqual(data, None)

        self.assertIn("id", data)
        self.assertEqual(data["id"], rec.id)
        self.assertIn("product_id", data)
        self.assertEqual(data["product_id"], rec.product_id)
        self.assertIn("rec_product_id", data)
        self.assertEqual(data["rec_product_id"], rec.rec_product_id)
        self.assertIn("type", data)
        self.assertEqual(data["type"], rec.type.name)

    def test_deserialize_a_recommendation(self):
        """Test deserialization of a Recommendation"""
        data = {
            "id": 1,
            "product_id": 50,
            "rec_product_id": 150,
            "type": "Generic",
            "interested": 6
        }
        rec = Recommendation()
        rec.deserialize(data)
        self.assertNotEqual(rec, None)
        self.assertEqual(rec.id, None)

        self.assertEqual(data["product_id"], 50)
        self.assertEqual(data["rec_product_id"], 150)
        self.assertEqual(data["interested"], 6)

        self.assertEqual(rec.type, RecommendationType.Generic)

    def test_deserialize_missing_data(self):
        """Test deserialization of a Recommendation with missing data"""
        data = {"id": 1, "product_id": 1, "type": "Generic"}
        rec = Recommendation()
        self.assertRaises(DataValidationError, rec.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        rec = Recommendation()
        self.assertRaises(DataValidationError, rec.deserialize, data)

    def test_deserialize_bad_type(self):
        """ Test deserialization of bad Recommendation Type attribute """
        test_rec = RecommendationFactory()
        data = test_rec.serialize()
        data["type"] = "Does't Exist"  # wrong case
        rec = Recommendation()
        self.assertRaises(DataValidationError, rec.deserialize, data)

    def test_deserialize_bad_product_id(self):
        """ Test deserialization of bad Query Product ID attribute """
        test_rec = RecommendationFactory()
        data = test_rec.serialize()
        data["product_id"] = "1234"  # wrong datatype
        rec = Recommendation()
        self.assertRaises(DataValidationError, rec.deserialize, data)

    def test_deserialize_bad_rec_product_id(self):
        """ Test deserialization of bad Recommended Product ID attribute """
        test_rec = RecommendationFactory()
        data = test_rec.serialize()
        data["rec_product_id"] = "1234"  # wrong datatype
        rec = Recommendation()
        self.assertRaises(DataValidationError, rec.deserialize, data)

    def test_deserialize_bad_interested(self):
        """ Test deserialization of bad interested attribute """
        test_rec = RecommendationFactory()
        data = test_rec.serialize()
        data["interested"] = "1234"  # wrong datatype
        rec = Recommendation()
        self.assertRaises(DataValidationError, rec.deserialize, data)

    def test_find_rec(self):
        """Find a Recommendation by ID"""
        recs = RecommendationFactory.create_batch(3)
        for rec in recs:
            rec.create()
        logging.debug(recs)
        self.assertEqual(len(Recommendation.all()), 3)

        rec = Recommendation.find(recs[1].id)
        self.assertIsNot(rec, None)
        self.assertEqual(rec.id, recs[1].id)

        self.assertEqual(rec.product_id, recs[1].product_id)
        self.assertEqual(rec.rec_product_id, recs[1].rec_product_id)
        self.assertEqual(rec.type, recs[1].type)

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        recs = RecommendationFactory.create_batch(3)
        for rec in recs:
            rec.create()

        rec = Recommendation.find_or_404(recs[1].id)
        self.assertIsNot(rec, None)
        self.assertEqual(rec.id, recs[1].id)
        self.assertEqual(rec.product_id, recs[1].product_id)
        self.assertEqual(rec.rec_product_id, recs[1].rec_product_id)
        self.assertEqual(rec.type, recs[1].type)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Recommendation.find_or_404, 0)

    def test_find_by_type(self):
        """Find Recommedations by Recommendation Type"""
        Recommendation(product_id=1, rec_product_id=5,
                       type=RecommendationType.Generic).create()
        Recommendation(product_id=1, rec_product_id=10,
                       type=RecommendationType.Generic).create()
        Recommendation(product_id=2, rec_product_id=5,
                       type=RecommendationType.Generic).create()

        res = Recommendation.find_rec_by_filter(type=RecommendationType.Generic)
        recs = [rec for rec in res]

        self.assertEqual(len(recs), 3)
        self.assertEqual(recs[0].product_id, 1)
        self.assertEqual(recs[0].rec_product_id, 5)
        self.assertEqual(recs[0].type, RecommendationType.Generic)

    def test_find_by_product_id(self):
        """Find Recommedations by Query Product ID"""
        Recommendation(product_id=1, rec_product_id=5,
                       type=RecommendationType.Generic).create()
        Recommendation(product_id=1, rec_product_id=10,
                       type=RecommendationType.UpSell).create()
        Recommendation(product_id=2, rec_product_id=5,
                       type=RecommendationType.CrossSell).create()

        res = Recommendation.find_rec_by_filter(product_id=2)
        recs = [rec for rec in res]

        self.assertEqual(recs[0].product_id, 2)
        self.assertEqual(recs[0].rec_product_id, 5)
        self.assertEqual(recs[0].type, RecommendationType.CrossSell)

    def test_find_by_rec_product_id(self):
        """Find Recommedations by Recommended Product ID"""
        Recommendation(product_id=1, rec_product_id=5,
                       type=RecommendationType.Generic).create()
        Recommendation(product_id=1, rec_product_id=10,
                       type=RecommendationType.UpSell).create()
        Recommendation(product_id=2, rec_product_id=5,
                       type=RecommendationType.CrossSell).create()

        res = Recommendation.find_rec_by_filter(rec_product_id=10)
        recs = [rec for rec in res]

        self.assertEqual(recs[0].rec_product_id, 10)
        self.assertEqual(recs[0].type, RecommendationType.UpSell)

    def test_find_by_product_id_and_type(self):
        """Find Recommedations by Query Product ID and Type"""

        Recommendation(product_id=1, rec_product_id=2,
                       type=RecommendationType.UpSell).create()
        Recommendation(product_id=1, rec_product_id=3,
                       type=RecommendationType.UpSell).create()
        Recommendation(product_id=1, rec_product_id=4,
                       type=RecommendationType.Generic).create()

        res = Recommendation.find_rec_by_filter(product_id=1, type=RecommendationType.UpSell)
        recs = [rec for rec in res]
        self.assertEqual(recs[0].product_id, 1)
        self.assertEqual(recs[0].rec_product_id, 2)
        self.assertEqual(recs[0].type, RecommendationType.UpSell)

    def test_find_by_rec_product_id_and_type(self):
        """Find Recommedations by Recommended Product ID and Type"""

        Recommendation(product_id=1, rec_product_id=3,
                       type=RecommendationType.UpSell).create()
        Recommendation(product_id=2, rec_product_id=3,
                       type=RecommendationType.UpSell).create()
        Recommendation(product_id=1, rec_product_id=4,
                       type=RecommendationType.Generic).create()

        res = Recommendation.find_rec_by_filter(rec_product_id=3, type=RecommendationType.UpSell)
        recs = [rec for rec in res]
        self.assertEqual(recs[0].rec_product_id, 3)
        self.assertEqual(recs[0].type, RecommendationType.UpSell)
