# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber


class TestReadSubscriptions(BaseTestCase):
    route = '/user/{}/subscriptions'

    def test_read_subscriptions(self):
        # Create a user
        user = UserFactory()

        # Create some communities
        communities = CommunityFactory.create_batch(5)

        # Make the user subscribe to the communities
        for community in communities:
            CommunitySubscriber(community=community, user=user).save()

        # Get user subscriptions
        response = self.client.get(self.route.format(user.username))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert that the response data length is 5
        self.assertEqual(len(data), 5)

       

    def test_read_subscriptions_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user subscriptions
        response = self.client.get(self.route.format(user.username))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])

    def test_read_subscriptions_nonexistent_user(self):
        # Try to get subscriptions of a nonexistent user
        response = self.client.get(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert that message
        self.assertEqual(data['message'], 'User not found.')
