# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token


class TestReadCommunities(BaseTestCase):
    route = '/community/'

    def test_read_community(self):
        # Create multiple communities
        communities = CommunityFactory.create_batch(size=5)

        # Get the communities
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the number of communities
        self.assertEqual(len(data), len(communities))

        # Assert each community
        for i, community in enumerate(communities):
            self.assertEqual(data[i]['id'], community.id)
            self.assertEqual(data[i]['name'], community.name)
            self.assertEqual(data[i]['about'], community.about)
            self.assertEqual(data[i]['created_at'], community.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
            self.assertEqual(data[i]['updated_at'], community.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_community_empty(self):
        # Get the communities
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the community
        self.assertEqual(len(data), 0)
