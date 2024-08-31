# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Follow
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadBlocked(BaseTestCase):
    route = '/user/blocked'

    def test_read_blocked(self):
        # Number of blocked users
        n = 5

        # create a user
        user = UserFactory()

        # Create some users to block
        users = UserFactory.create_batch(n)

        # Block all users
        for u in users:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the blocked
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data
        self.assertEqual(len(data), n)

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

    def test_read_blocked_no_blocked_users(self):
        # create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Get the blocked
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data
        self.assertEqual(len(data), 0)

        