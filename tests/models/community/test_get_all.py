# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import Community

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetCommunities(BaseTestCase):
    def test_get_communities(self):
        # Number of communities
        n = 5

        # Create some communities
        communities = CommunityFactory.create_batch(n)

        # Set the args
        args = {}

        # get communities
        communities = Community.get_all(args)

        # Assert communities is a Pagination object
        self.assertIsInstance(communities, Pagination)

        # Get the items
        communities = communities.items

        # Assert communities is a list
        self.assertIsInstance(communities, list)

        # Assert the number of communities
        self.assertEqual(len(communities), n)

        # Assert the communities are the same
        self.assertEqual(communities, communities)

    def test_get_communities_empty(self):
        # Set the args
        args = {}

        # get communities
        communities = Community.get_all(args)

        # Assert communities is a Pagination object
        self.assertIsInstance(communities, Pagination)

        # Get the items
        communities = communities.items

        # Assert communities is a list
        self.assertIsInstance(communities, list)

        # Assert the number of communities
        self.assertEqual(len(communities), 0)

        # Assert communities is empty
        self.assertEqual(communities, [])



