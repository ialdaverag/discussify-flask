# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.community_factory import CommunityFactory


class TestReadCommunities(BaseTestCase):
    route = '/community/'

    def test_read_community(self):
        # Number of communities
        n = 5

        # Create multiple communities
        CommunityFactory.create_batch(n)

        # Get the communities
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the number of communities
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for community in data:
            self.assertIn('id', community)
            self.assertIn('name', community)
            self.assertIn('about', community)
            self.assertIn('owner', community)
            self.assertIn('owned_by', community)
            self.assertIn('subscriber', community)
            self.assertIn('moderator', community)
            self.assertIn('ban', community)
            self.assertIn('stats', community)
            self.assertIn('created_at', community)
            self.assertIn('updated_at', community)

    def test_read_community_empty(self):
        # Get the communities
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the community
        self.assertEqual(len(data), 0)
