# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.post_factory import PostFactory
from tests.factories.comment_factory import CommentFactory


class TestReadComments(BaseTestCase):
    route = '/post/{}/comments'

    def test_read_comments(self):
        # Number of comments
        n = 5

        # Create a post
        post = PostFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n, post=post)

        # Get the comments
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of comments
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
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)

    def test_read_comments_empty(self):
        # Create a post
        post = PostFactory()

        # Get the comments
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])