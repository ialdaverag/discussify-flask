# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestReadFollowed(BaseTestCase):
    route = '/user/{}/following'

    def test_read_followed(self):
        # Create a user
        user = UserFactory()

       # Create some followed users
        followed = UserFactory.create_batch(5)

        # Make the user follow the followed users
        for user_ in followed:
            user_.append_follower(user)

        # Get user followed
        response = self.client.get(self.route.format(user.username))

        # Assert the response status
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, list)

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
