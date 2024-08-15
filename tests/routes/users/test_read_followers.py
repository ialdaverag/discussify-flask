# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Follow


class TestReadFollowers(BaseTestCase):
    route = '/user/{}/followers'

    def test_read_followers(self):
        # Number of followers
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followers
        followers = UserFactory.create_batch(n)

        # Make the followers follow the user
        for follower in followers:
            Follow(follower=follower, followed=user).save()

        # Get user followers
        response = self.client.get(self.route.format(user.username))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of followers
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for user_ in data:
            self.assertIn('id', user_)
            self.assertIn('username', user_)
            self.assertIn('email', user_)
            self.assertIn('following', user_)
            self.assertIn('follower', user_)
            self.assertIn('stats', user_)
            self.assertIn('created_at', user_)
            self.assertIn('updated_at', user_)

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
