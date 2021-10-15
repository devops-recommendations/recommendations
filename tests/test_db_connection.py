"""
TestYourResourceModel API Service Test Suite
Test cases can be run with:
    nosetests
    coverage report -m
While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_pets.py:TestPetModel
# """
# import os
# import logging
# import unittest
# from werkzeug.exceptions import NotFound
# from service import app

from flask.ext.testing import TestCase
from myapp import create_app, db

######################################################################
#  T E S T   D A T A   B A S E  
######################################################################

class MyTest(TestCase):

    DATABASE_URI = os.getenv("DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb")
    TESTING = True

    def create_app(self):
        # pass in test configuration
        return create_app(self)

    def setUp(self):
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
