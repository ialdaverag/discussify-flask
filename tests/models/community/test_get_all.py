# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import Community


class TestGetAll(BaseTestCase):
    def test_get_all(self):
        # Number of communities to create
        n = 5

        # Create a community
        CommunityFactory.create_batch(n)

        # Get all communities
        communities = Community.get_all()

        # Assert the number of communities
        self.assertEqual(len(communities), n)

    def test_get_all_empty(self):
        # Get all communities
        communities = Community.get_all()

        # Assert that communities is an empty list
        self.assertEqual(communities, [])