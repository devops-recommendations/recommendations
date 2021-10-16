# This file uses John Rofrano's git repositoy: https://github.com/nyu-devops/lab-flask-tdd

"""
Models for Recommendation Service

All of the models are stored in this module

Models
------
Pet - A Pet used in the Pet Store

Attributes:
-----------
query_prod_id (string) - the name of the pet
 (string) - the category the pet belongs to (i.e., dog, cat)
available (boolean) - True for pets that are available for adoption

"""
import logging
from enum import Enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    """Initialies the SQLAlchemy app"""
    Recommendation.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""

    pass


class RecommendationType(Enum):
    """Enumeration of valid Pet Genders"""
    Generic = 0
    BoughtTogether = 1
    Complementary = 4
    CrossSell = 2
    UpSell = 3

class Recommendation(db.Model):
    """
    Class that represents a Recommendation

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    app:Flask=None

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    query_prod_id = db.Column(db.String(63), nullable=False)
    rec_prod_id = db.Column(db.String(63), nullable=False)
    type = db.Column(
        db.Enum(RecommendationType), nullable=False, server_default=(RecommendationType.Generic.name)
    )

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Recommendation of prod=[%d] is prod=[%d] with id=[%s] in table>" % (self.query_prod_id, self.rec_prod_id, self.id)

    def create(self):
        """
        Creates a Recommendation in the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Recommendation to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes a Recommendation from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict:
        """Serializes a Recommendation into a dictionary"""
        return {
            "id": self.id,
            "query_prod_id": self.query_prod_id,
            "rec_prod_id": self.rec_prod_id,
            "type": self.type
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Recommendation from a dictionary
        Args:
            data (dict): A dictionary containing the Recommendation data
        """
        try:
            if isinstance(data['query_prod_id'], int):
                self.query_prod_id = data["query_prod_id"]
            else:
                raise DataValidationError("Invalid Query Product ID: " + data['query_prod_id'])    
            if isinstance(data['rec_prod_id'], int):
                self.rec_prod_id = data["rec_prod_id"]
            else:
                raise DataValidationError("Invalid Query Product ID: " + data['query_prod_id'])  
            self.type = getattr(RecommendationType, data["type"])

        except AttributeError as error:
            raise DataValidationError("Invalid Recommendation Type: " + error.args[0])
        except KeyError as error:
            raise DataValidationError("Invalid Recommendation: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Recommendation: body of request contained bad or no data"
            )
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app:Flask):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls) -> list:
        """Returns all of the Recommendation in the database"""
        logger.info("Processing all Recommendations")
        return cls.query.all()

    @classmethod
    def find(cls, rec_id:int):
        """Finds a Recommendation by it's ID

        :param rec_id: the id of the Recommendation to find
        :type rec_id: int

        :return: an instance with the rec_id, or None if not found
        :rtype: Recommendation

        """
        logger.info("Processing lookup for id %s ...", rec_id)
        return cls.query.get(rec_id)

    @classmethod
    def find_or_404(cls, rec_id:int):
        """Find a Recommendation by it's id

        :param rec_id: the id of the rec to find
        :type rec_id: int

        :return: an instance with the rec_id, or 404_NOT_FOUND if not found
        :rtype: Recommendation

        """
        logger.info("Processing lookup or 404 for id %s ...", rec_id)
        return cls.query.get_or_404(rec_id)

    @classmethod
    def get_by_prod_id(cls, query_prod_id:int) -> list:
        """Returns all Recommendations for a given product

        :param prod_id: the prod_id of Query Product whose Recommendations you want
        :type prod_id: int

        :return: a collection of Recommendations for a query prod_id
        :rtype: list

        """
        logger.info("Processing name query for %s ...", query_prod_id)
        return cls.query.filter(cls.query_prod_id == query_prod_id)

    @classmethod
    def get_by_prod_id_and_type(cls, query_prod_id: int, type: RecommendationType = RecommendationType.Generic) -> list:
        """Returns all of the Recommendations for query product of a given type

        :param 
            query_prod_id: the product_id of the product for which you want recommendations
            type: the type of the recommendation you want to retrieve
        :type 
            query_prod_id: int
            type: RecommendationType

        :return: a collection of Recommendations for query_prod_id and of type
        :rtype: list

        """
        logger.info("Processing prod_id and type query for %s %s...", query_prod_id, type.name)
        return cls.query.filter(cls.query_prod_id == query_prod_id, cls.type == type)