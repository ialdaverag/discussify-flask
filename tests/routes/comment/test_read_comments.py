# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory


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

    def test_read_commens_empty(self):
        # Get the comments
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the community
        self.assertEqual(len(data), 0)