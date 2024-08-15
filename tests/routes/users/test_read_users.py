# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestReadUsers(BaseTestCase):
    route = '/user/'

    def test_read_users(self):
        # Create multiple users using batch
        users = UserFactory.create_batch(size=5)

        # Get the users
        response = self.client.get(self.route)

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the number of users
        self.assertEqual(len(data), len(users))

        # Assert the response data structure
        for user in data:
            self.assertIn('id', user)
            self.assertIn('username', user)
            self.assertIn('email', user)
            self.assertIn('following', user)
            self.assertIn('follower', user)
            self.assertIn('stats', user)
            self.assertIn('created_at', user)
            self.assertIn('updated_at', user)

    def test_read_users_empty(self):
        # Get the users
        response = self.client.get(self.route)

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the response data
        self.assertEqual(data, [])
