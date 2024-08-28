# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestDeleteComment(BaseTestCase):
    route = '/comment/'

    def test_read_comments(self):
        # Create multiple comments
        comments = CommentFactory.create_batch(size=5)

        # Get the comments
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of comments
        self.assertEqual(len(data), len(comments))

        # Assert each comment
        for comment in data:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('owner', comment)
            self.assertIn('post', comment)
            self.assertIn('bookmarked', comment)
            self.assertIn('upvoted', comment)
            self.assertIn('downvoted', comment)
            self.assertIn('replies', comment)
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)

    def test_read_comments_authenticated(self):
        # Create a user
        user = UserFactory()

        # Create multiple comments
        comments = CommentFactory.create_batch(size=5)

        # Get user access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of comments
        self.assertEqual(len(data), len(comments))

        # Assert each comment
        for comment in data:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('owner', comment)
            self.assertIn('post', comment)
            self.assertIn('bookmarked', comment)
            self.assertIn('upvoted', comment)
            self.assertIn('downvoted', comment)
            self.assertIn('replies', comment)
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)

    def test_read_comments_with_blocked(self):
        # Number of comments
        n = 5

        # Create multiple comments
        comments = CommentFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Create a user
        user = UserFactory()

        # Block some users
        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the comments
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

        # Assert the number of comments
        self.assertEqual(len(data), n - b)

        # Assert each comment
        for comment in data:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('owner', comment)
            self.assertIn('post', comment)
            self.assertIn('bookmarked', comment)
            self.assertIn('upvoted', comment)
            self.assertIn('downvoted', comment)
            self.assertIn('replies', comment)
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)

    def test_read_comments_with_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the comments
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

        # Assert the number of comments
        self.assertEqual(len(data), n - b)

        # Assert each comment
        for comment in data:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('owner', comment)
            self.assertIn('post', comment)
            self.assertIn('bookmarked', comment)
            self.assertIn('upvoted', comment)
            self.assertIn('downvoted', comment)
            self.assertIn('replies', comment)
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)

    def test_read_comments_with_blocked_and_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Block some users
        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Number of blockers
        c = 2

        # Block some users
        for comment in comments[-c:]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the comments
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

        # Assert the number of comments
        self.assertEqual(len(data), n - b - c)

    def test_read_comments_empty(self):
        # Get the comments
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the community
        self.assertEqual(len(data), 0)