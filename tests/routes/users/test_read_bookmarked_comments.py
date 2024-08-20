# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory

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