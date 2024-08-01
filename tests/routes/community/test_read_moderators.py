# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token


class TestReadModerators(BaseTestCase):
    route = '/community/{}/moderators'

    def test_read_moderators(self):
        # Create multiple moderators
        moderators = UserFactory.create_batch(size=5)

        # Create a community
        community = CommunityFactory()

        # Append the moderators to the community
        for moderator in moderators:
            community.append_subscriber(moderator)

        # Read the community moderators
        response = self.client.get(self.route.format(community.name))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

    def test_read_moderators_empty(self):
        # Create a community
        community = CommunityFactory()

        # Read the community moderators
        response = self.client.get(self.route.format(community.name))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])

    def test_read_moderators_nonexistent_community(self):
        # Try to get moderators of a nonexistent community
        response = self.client.get(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')
