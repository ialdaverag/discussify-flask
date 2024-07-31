# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestReadFollowers(BaseTestCase):
    route = '/user/{}/followers'

    def test_read_followers(self):
        # Create a user
        user = UserFactory()

        # Create some followers
        followers = UserFactory.create_batch(5)

        # Make the followers follow the user
        for follower in followers:
            user.append_follower(follower)

        # Get user followers
        response = self.client.get(self.route.format(user.username))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

    def test_read_followers_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user followers
        response = self.client.get(self.route.format(user.username))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])

    def test_read_followers_nonexistent_user(self):
        # Try to get followers of a nonexistent user
        response = self.client.get(self.route.format('inexistent'))

        # Assert that the response status code is 404
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert that the error message is 'User not found.'
        self.assertEqual(data['message'], 'User not found.')
