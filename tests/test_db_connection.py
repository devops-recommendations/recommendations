"""
TestYourResourceModel API Service Test Suite
Test cases can be run with:
    nosetests
    coverage report -m
While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_pets.py:TestPetModel
"""
import os
import logging
import unittest
from werkzeug.exceptions import NotFound
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  T E S T   D A T A   B A S E  
######################################################################

class TestPetModel(unittest.TestCase):
    """Test Cases for Pet Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        pass
