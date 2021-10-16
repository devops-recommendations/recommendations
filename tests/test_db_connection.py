"""
Test cases for DB Connection
Test cases can be run with:
    nosetests
    coverage report -m
While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_db_connection.py:TestDBConnection
"""
import os
import logging
import unittest
from service import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Disable all but ciritcal errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)
db = SQLAlchemy()

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)

class TestDBConnection(unittest.TestCase):
    """Test Cases for DB Connection"""

    app:Flask= None

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
    
    def test_connection(self):
        """Test to check if DB is alive"""        
        db.init_app(app)
        app.app_context().push()
        
        self.assertEquals(db.drop_all(), None)

        
        
        
    