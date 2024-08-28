# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Managers
from app.models.comment import CommentVote

# Models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadUpvotedComments(BaseTestCase):
    route = '/user/comments/upvoted'

    def test_read_upvoted_comments(self):
        # Nmber of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n)

        # Assert the response data structure
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

    def test_read_upvoted_comments_with_blocked(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
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

    def test_read_upvoted_comments_with_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
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

    def test_read_upvoted_comments_with_blocked_and_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Number of blockers users
        c = 2

        for comment in comments[-c:]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n - b - c)

        # Assert the response data structure
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
            
    def test_read_upvoted_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user upvoted comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])