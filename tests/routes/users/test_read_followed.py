# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Follow
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


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
        for user in data:
            self.assertIn('id', user)
            self.assertIn('username', user)
            self.assertIn('email', user)
            self.assertIn('following', user)
            self.assertIn('follower', user)
            self.assertIn('stats', user)
            self.assertIn('created_at', user)
            self.assertIn('updated_at', user)

    def test_read_followed_authenticated(self):
        # Number of followed users
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followed users
        followed = UserFactory.create_batch(n)

        # Make the user follow the followed users
        for user_ in followed:
            Follow(follower=user, followed=user_).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get user followed
        response = self.client.get(
            self.route.format(user.username), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, list)

        # Assert the response data length
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

    def test_read_followers_with_blocked(self):
        # Number of users
        n = 5

        # Number of blocked users
        b = 2

        # Number of followers
        f = 3

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Make the first 3 users follow the user
        for u in users[:f]:
            Follow(follower=user, followed=u).save()

        # Block the last 2 users
        for u in users[-b:]:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route.format(user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the number of users
        self.assertEqual(len(data), n - b)

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

    def test_read_followers_with_blockers(self):
        # Number of users
        n = 5

        # Number of blockers
        b = 2

        # Number of followers
        f = 3

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Make the first 3 users follow the user
        for u in users[:f]:
            Follow(follower=user, followed=u).save()

        # Block the last 2 users
        for u in users[-b:]:
            Block(blocker=u, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route.format(user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the number of users
        self.assertEqual(len(data), n - b)

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
