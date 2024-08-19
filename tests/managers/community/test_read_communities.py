# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Managers
from app.managers.community import CommunityManager


class TestReadCommunities(BaseTestCase):
    def test_read_communities(self):
        # Number of communities
        n = 5

        # Create some communities
        communities = CommunityFactory.create_batch(n)

        # Read communities
        communities_to_read = CommunityManager.read_all()

        # Assert the number of communities
        self.assertEqual(len(communities_to_read), n)

        # Assert the communities are the same
        self.assertEqual(communities, communities_to_read)

    def test_read_communities_empty(self):
        # Read communities
        communities = CommunityManager.read_all()

        # Assert the number of communities
        self.assertEqual(len(communities), 0)

        # Assert that the communities are an empty list
        self.assertEqual(communities, [])


