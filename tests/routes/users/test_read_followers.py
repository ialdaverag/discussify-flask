# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Follow
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


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

    def test_read_followers_authenticated(self):
        # Number of followers
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followers
        followers = UserFactory.create_batch(n)

        # Make the followers follow the user
        for follower in followers:
            Follow(follower=follower, followed=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get user followers
        response = self.client.get(
            self.route.format(user.username), 
            headers={'Authorization': access_token}
        )

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
            Follow(follower=u, followed=user).save()

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

    def test_read_follwoers_with_blockers(self):
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
            Follow(follower=u, followed=user).save()

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

    def test_read_followers_with_blocked_and_blockers(self):
        # Number of users
        n = 10

        # Number of blocked users
        m = 2

        # Number of blockers
        o = 2

        # Number of followers
        f = n - m - o

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block the first 2 users
        for u in users[:m]:
            Block(blocker=user, blocked=u).save()

        # Block the last 2 users
        for u in users[-o:]:
            Block(blocker=u, blocked=user).save()

        # Make the remaining users follow the user
        for u in users[m:n-o]:
            Follow(follower=u, followed=user).save()

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
        self.assertEqual(len(data), f)

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
