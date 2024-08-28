# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadBookmarkedComments(BaseTestCase):
    route = '/user/comments/bookmarked'

    def test_read_bookmarked_comments(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarked comments
        CommentBookmarkFactory.create_batch(n, user=user)

        # Get user access token
        access_token = get_access_token(user)

        # Get user bookmarked comments
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

        # Assert the number of bookmarks
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

    def test_read_bookmarked_comments_with_blocked(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = CommentBookmarkFactory.create_batch(n, user=user)

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.comment.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
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

        # Assert the number of bookmarks
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

    def test_read_bookmarked_comments_with_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = CommentBookmarkFactory.create_batch(n, user=user)

        # Number of blocking users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=bookmark.comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
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

        # Assert the number of bookmarks
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

    def test_read_bookmarked_comments_with_blocked_and_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = CommentBookmarkFactory.create_batch(n, user=user)

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.comment.owner).save()

        # Number of blocking users
        c = 2

        for bookmark in bookmarks[-c:]:
            Block(blocker=bookmark.comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
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

        # Assert the number of bookmarks
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

    def test_read_bookmarked_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
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