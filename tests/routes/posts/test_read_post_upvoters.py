# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token


class TestReadPostUpvoters(BaseTestCase):
    route = '/post/{}/upvoters'

    def test_read_post_upvoters(self):
        # Number of upvoters
        n = 5

        # Create a post
        post = PostFactory()

        # Create some upvoters
        PostVoteFactory.create_batch(n, post=post, direction=1)

        # Get the upvoters
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for upvoter in data:
            self.assertIn('id', upvoter)
            self.assertIn('username', upvoter)
            self.assertIn('email', upvoter)
            self.assertIn('following', upvoter)
            self.assertIn('follower', upvoter)
            self.assertIn('stats', upvoter)
            self.assertIn('created_at', upvoter)
            self.assertIn('updated_at', upvoter)

    def test_read_post_upvoters_authenticated(self):
        # Number of upvoters
        n = 5

        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Create some upvoters
        PostVoteFactory.create_batch(n, post=post, direction=1)

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for upvoter in data:
            self.assertIn('id', upvoter)
            self.assertIn('username', upvoter)
            self.assertIn('email', upvoter)
            self.assertIn('following', upvoter)
            self.assertIn('follower', upvoter)
            self.assertIn('stats', upvoter)
            self.assertIn('created_at', upvoter)
            self.assertIn('updated_at', upvoter)

    def test_read_post_upvoters_with_blocked(self):
        # Number of upvoters
        n = 5

        # Number of blocked upvoters
        b = 3

        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Create some upvoters
        upvoters = PostVoteFactory.create_batch(n, post=post, direction=1)

        # Block  the first 3 upvoters
        for upvoter in upvoters[:b]:
            Block(blocker=user, blocked=upvoter.user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for upvoter in data:
            self.assertIn('id', upvoter)
            self.assertIn('username', upvoter)
            self.assertIn('email', upvoter)
            self.assertIn('following', upvoter)
            self.assertIn('follower', upvoter)
            self.assertIn('stats', upvoter)
            self.assertIn('created_at', upvoter)
            self.assertIn('updated_at', upvoter)

    def test_read_post_upvoters_with_blockers(self):
        # Number of upvoters
        n = 5

        # Number of blockers
        b = 3

        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Create some upvoters
        upvoters = PostVoteFactory.create_batch(n, post=post, direction=1)

        # Block the user from the first 3 upvoters
        for upvoter in upvoters[:b]:
            Block(blocker=upvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for upvoter in data:
            self.assertIn('id', upvoter)
            self.assertIn('username', upvoter)
            self.assertIn('email', upvoter)
            self.assertIn('following', upvoter)
            self.assertIn('follower', upvoter)
            self.assertIn('stats', upvoter)
            self.assertIn('created_at', upvoter)
            self.assertIn('updated_at', upvoter)

    def test_read_post_upvoters_with_blocked_and_blockers(self):
        # Number of upvoters
        n = 5

        # Number of blocked upvoters
        b = 2

        # Number of blockers
        c = 2

        # Create a post
        post = PostFactory()

        # Create some upvoters
        upvoters = PostVoteFactory.create_batch(n, post=post, direction=1)

        # Create a user
        user = UserFactory()

        # Block the upvoters
        for upvoter in upvoters[:b]:
            Block(blocker=user, blocked=upvoter.user).save()

        # Block the user
        for upvoter in upvoters[-c:]:
            Block(blocker=upvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n - b - c)

        # Assert the response data structure
        for upvoter in data:
            self.assertIn('id', upvoter)
            self.assertIn('username', upvoter)
            self.assertIn('email', upvoter)
            self.assertIn('following', upvoter)
            self.assertIn('follower', upvoter)
            self.assertIn('stats', upvoter)
            self.assertIn('created_at', upvoter)
            self.assertIn('updated_at', upvoter)

    def test_read_post_upvoters_empty(self):
        # Create a post
        post = PostFactory()

        # Get the upvoters
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of upvoters
        self.assertEqual(len(data), 0)

    def test_read_post_upvoters_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(404),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 404)
