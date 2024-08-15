# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Follow


class TestReadFollowed(BaseTestCase):
    route = '/user/{}/following'

    def test_read_followed(self):
        # Number of followed users
        n = 5

        # Create a user
        user = UserFactory()

       # Create some followed users
        followed = UserFactory.create_batch(n)

        # Make the user follow the followed users
        for user_ in followed:
            Follow(follower=user, followed=user_).save()

        # Get user followed
        response = self.client.get(self.route.format(user.username))

        # Assert the response status
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, list)

        # Assert the response data length
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

    def test_read_followed_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user followed
        response = self.client.get(self.route.format(user.username))

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the response data
        self.assertEqual(data, [])

    def test_read_followed_nonexistent_user(self):
        # Try to get followed users of a nonexistent user
        response = self.client.get(self.route.format('inexistent'))

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert the error message
        self.assertEqual(data['message'], 'User not found.')
