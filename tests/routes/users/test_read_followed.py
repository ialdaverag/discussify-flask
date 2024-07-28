# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestReadFollowed(BaseTestCase):
    route = '/user/<string:username>/following'

    def test_read_followed(self):
        # Create a user
        user = UserFactory()

       # Create some followed users
        followed = UserFactory.create_batch(5)

        # Make the user follow the followed users
        for user_ in followed:
            user_.append_follower(user)

        # Get user followed
        response = self.client.get(f'/user/{user.username}/following')

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

    def test_read_followed_nonexistent_user(self):
        # Try to get followed users of a nonexistent user
        response = self.client.get('/user/inexistent/following')

        # Assert that the response status code is 404
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert that the error message is 'User not found.'
        self.assertEqual(data['message'], 'User not found.')

    def test_read_followed_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user followed
        response = self.client.get(f'/user/{user.username}/following')

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])
