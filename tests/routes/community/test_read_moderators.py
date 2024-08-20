# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityModerator


class TestReadModerators(BaseTestCase):
    route = '/community/{}/moderators'

    def test_read_moderators(self):
        # Number of moderators
        n = 5

        # Create multiple moderators
        moderators = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the moderators to the community
        for moderator in moderators:
            CommunityModerator(community=community, user=moderator).save()

        # Read the community moderators
        response = self.client.get(self.route.format(community.name))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for moderator in data:
            self.assertIn('id', moderator)
            self.assertIn('username', moderator)
            self.assertIn('email', moderator)
            self.assertIn('following', moderator)
            self.assertIn('follower', moderator)
            self.assertIn('stats', moderator)
            self.assertIn('created_at', moderator)
            self.assertIn('updated_at', moderator)
        

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
