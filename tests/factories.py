
"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Recommendation, RecommendationType


class RecommendationFactory(factory.Factory):
    """Creates fake recommendations that you don't have to feed"""

    class Meta:
        model = Recommendation
    
    id = factory.Sequence(lambda n: n)
    query_prod_id = FuzzyChoice(choices=[i for i in range(100)])
    rec_prod_id = FuzzyChoice(choices=[i for i in range(100, 200)])
    type = FuzzyChoice(choices=list(RecommendationType))