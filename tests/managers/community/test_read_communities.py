# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Managers
from app.managers.community import CommunityManager

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadCommunities(BaseTestCase):
    def test_read_communities(self):
        # Number of communities
        n = 5

        # Create some communities
        communities = CommunityFactory.create_batch(n)

        # Set the args
        args = {}

        # Read communities
        communities_to_read = CommunityManager.read_all(args)

        # Assert communities_to_read is a Pagination object
        self.assertIsInstance(communities_to_read, Pagination)

        # Get the items
        communities_to_read = communities_to_read.items

        # Assert communities_to_read is a list
        self.assertIsInstance(communities_to_read, list)

        # Assert the number of communities
        self.assertEqual(len(communities_to_read), n)

        # Assert the communities are the same
        self.assertEqual(communities, communities_to_read)

    def test_read_communities_empty(self):
        # Set the args
        args = {}

        # Read communities
        communities_to_read = CommunityManager.read_all(args)

        # Assert communities_to_read is a Pagination object
        self.assertIsInstance(communities_to_read, Pagination)

        # Get the items
        communities_to_read = communities_to_read.items

        # Assert communities_to_read is a list
        self.assertIsInstance(communities_to_read, list)

        # Assert the number of communities
        self.assertEqual(len(communities_to_read), 0)

        # Assert communities_to_read is empty
        self.assertEqual(communities_to_read, [])



