# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.block_factory import BlockFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadUsers(BaseTestCase):
    route = '/user/'

    def test_read_users_anonymous(self):
        # Number of users
        n = 5

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Get the users
        response = self.client.get(self.route)

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the number of users
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

    def test_read_users_authenticated(self):
        # Number of users
        n = 5

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the number of users
        self.assertEqual(len(data), n + 1)

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

    def test_read_users_with_blocked(self):
        # Number of users
        n = 5

        # Number of blocked users
        m = 2

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block some users
        for u in users[:m]:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the number of users
        self.assertEqual(len(data), n - m + 1)

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

    def test_read_users_with_blockers(self):
        # Number of users
        n = 5

        # Number of blockers users
        m = 3

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block the user
        for u in users[:m]:
            Block(blocker=u, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the number of users
        self.assertEqual(len(data), n - m + 1)

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

    def test_read_users_with_blocked_and_blockers(self):
        # Number of users
        n = 5

        # Number of blocked users
        m = 1

        # Number of blockers users
        o = 1

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block some users
        for u in users[:m]:
            Block(blocker=user, blocked=u).save()

        # Block the user
        for u in users[m:m + o]:
            Block(blocker=u, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the number of users
        self.assertEqual(len(data), n - m - o + 1)

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
