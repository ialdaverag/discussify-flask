# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_vote_factory import CommentVoteFactory
from tests.factories.comment_factory import CommentFactory


class TestReadCommentDownvoters(BaseTestCase):
    route = '/comment/{}/downvoters'

    def test_read_comment_downvoters(self):
        # Number of downvoters
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Get the downvoters
        response = self.client.get(self.route.format(comment.id))

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of downvoters
        self.assertEqual(len(data), n)

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

    def test_read_comment_downvoters_empty(self):
        # Create a comment
        comment = CommentFactory()

        # Get the downvoters
        response = self.client.get(self.route.format(comment.id))

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of downvoters
        self.assertEqual(len(data), 0)

    def test_read_comment_downvoters_nonexistent(self):
        # Get the downvoters
        response = self.client.get(self.route.format(404))

        # Check status code
        self.assertEqual(response.status_code, 404)
