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


class TestReadPostDownvoters(BaseTestCase):
    route = '/post/{}/downvoters'

    def test_read_post_downvoters(self):
        # Number of downvoters
        n = 5

        # Create a post
        post = PostFactory()

        # Create some downvoters
        PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Get the downvoters
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
        for downvoter in data:
            self.assertIn('id', downvoter)
            self.assertIn('username', downvoter)
            self.assertIn('email', downvoter)
            self.assertIn('following', downvoter)
            self.assertIn('follower', downvoter)
            self.assertIn('stats', downvoter)
            self.assertIn('created_at', downvoter)
            self.assertIn('updated_at', downvoter)

    def test_read_post_downvoters_authenticated(self):
        # Number of downvoters
        n = 5

        # Create a post
        post = PostFactory()

        # Create some downvoters
        PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Get the downvoters
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
        for downvoter in data:
            self.assertIn('id', downvoter)
            self.assertIn('username', downvoter)
            self.assertIn('email', downvoter)
            self.assertIn('following', downvoter)
            self.assertIn('follower', downvoter)
            self.assertIn('stats', downvoter)
            self.assertIn('created_at', downvoter)
            self.assertIn('updated_at', downvoter)

    def test_read_post_downvoters_with_blocked(self):
        # Number of downvoters
        n = 5

        # Number of blocked downvoters
        b = 2

        # Create a post
        post = PostFactory()

        # Create some downvoters
        downvoters = PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=user, blocked=downvoter.user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
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
        for downvoter in data:
            self.assertIn('id', downvoter)
            self.assertIn('username', downvoter)
            self.assertIn('email', downvoter)
            self.assertIn('following', downvoter)
            self.assertIn('follower', downvoter)
            self.assertIn('stats', downvoter)
            self.assertIn('created_at', downvoter)
            self.assertIn('updated_at', downvoter)

    def test_read_post_downvoters_with_blockers(self):
        # Number of downvoters
        n = 5

        # Number of blockers
        b = 2

        # Create a post
        post = PostFactory()

        # Create some downvoters
        downvoters = PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the user
        for downvoter in downvoters[-b:]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
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
        for downvoter in data:
            self.assertIn('id', downvoter)
            self.assertIn('username', downvoter)
            self.assertIn('email', downvoter)
            self.assertIn('following', downvoter)
            self.assertIn('follower', downvoter)
            self.assertIn('stats', downvoter)
            self.assertIn('created_at', downvoter)
            self.assertIn('updated_at', downvoter)

    def test_read_post_downvoters_with_blocked_and_blockers(self):
        # Number of downvoters
        n = 5

        # Number of blocked downvoters
        b = 2

        # Number of blockers
        c = 2

        # Create a post
        post = PostFactory()

        # Create some downvoters
        downvoters = PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=user, blocked=downvoter.user).save()

        # Block the user
        for downvoter in downvoters[-c:]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
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
        for downvoter in data:
            self.assertIn('id', downvoter)
            self.assertIn('username', downvoter)
            self.assertIn('email', downvoter)
            self.assertIn('following', downvoter)
            self.assertIn('follower', downvoter)
            self.assertIn('stats', downvoter)
            self.assertIn('created_at', downvoter)
            self.assertIn('updated_at', downvoter)

    def test_read_post_downvoters_empty(self):
        # Create a post
        post = PostFactory()

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of downvoters
        self.assertEqual(len(data), 0)

        # Assert the response data structure
        for downvoter in data:
            self.assertIn('id', downvoter)
            self.assertIn('username', downvoter)
            self.assertIn('email', downvoter)
            self.assertIn('following', downvoter)
            self.assertIn('follower', downvoter)
            self.assertIn('stats', downvoter)
            self.assertIn('created_at', downvoter)
            self.assertIn('updated_at', downvoter)

    def test_read_post_downvoters_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the downvoters
        response = self.client.get(self.route.format(404))

        # Check status code
        self.assertEqual(response.status_code, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Post not found.')
