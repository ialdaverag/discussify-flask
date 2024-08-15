# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunitySubscriber

class TestReadSubscribers(BaseTestCase):
    route = '/community/{}/subscribers'

    def test_read_subscribers(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Read the community subscribers
        response = self.client.get(self.route.format(community.name))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for subscriber in data:
            self.assertIn('id', subscriber)
            self.assertIn('username', subscriber)
            self.assertIn('email', subscriber)
            self.assertIn('following', subscriber)
            self.assertIn('follower', subscriber)
            self.assertIn('stats', subscriber)
            self.assertIn('created_at', subscriber)
            self.assertIn('updated_at', subscriber)

    def test_read_subscribers_empty(self):
        # Create a community
        community = CommunityFactory()

        # Read the community subscribers
        response = self.client.get(self.route.format(community.name))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])

    def test_read_subscribers_nonexistent_community(self):
        # Try to get subscribers of a nonexistent community
        response = self.client.get(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')
