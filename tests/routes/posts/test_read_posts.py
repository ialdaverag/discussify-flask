# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.post_factory import PostFactory
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestDeletePost(BaseTestCase):
    route = '/post/'

    def test_read_posts(self):
        # Number of posts
        n = 5

        # Create multiple communities
        posts = PostFactory.create_batch(n)

        # Get the posts
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, list)

        # Assert the number of posts
        self.assertEqual(len(data), n)

        # Assert each post
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_posts_authenticated(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create multiple communities
        posts = PostFactory.create_batch(n)

        # Get user access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, list)

        # Assert the number of posts
        self.assertEqual(len(data), n)

        # Assert each post
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_posts_with_blocked(self):
        # Number of posts
        n = 5

        # Create multiple users using batch
        posts = PostFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Create a user
        user = UserFactory()

        # Block some users
        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, list)

        # Assert the number of posts
        self.assertEqual(len(data), n - b)

        # Assert each post
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_posts_with_blockers(self):
        # Number of posts
        n = 5

        # Create multiple users using batch
        posts = PostFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Create a user
        user = UserFactory()

        # Block some users
        for post in posts[:b]:
            Block(blocker=post.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, list)

        # Assert the number of posts
        self.assertEqual(len(data), n - b)

        # Assert each post
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_posts_with_blocked_and_blockers(self):
        # Number of posts
        n = 5

        # Create multiple users using batch
        posts = PostFactory.create_batch(n)

        # Create a user
        user = UserFactory()

        # Number of blocked users
        b = 2

        # Block some users
        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Number of blockers
        c = 2

        # Block some users
        for post in posts[-c:]:
            Block(blocker=post.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, list)

        # Assert the number of posts
        self.assertEqual(len(data), n - b - c)

    def test_read_posts_empty(self):
        # Get the posts
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the community
        self.assertEqual(len(data), 0)