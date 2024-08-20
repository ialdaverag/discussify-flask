# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory
from tests.factories.comment_factory import CommentFactory


class TestReadCommentUpvoters(BaseTestCase):
    route = '/comment/{}/upvoters'

    def test_read_comment_upvoters(self):
        # Number of upvoters
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Get the upvoters
        response = self.client.get(self.route.format(comment.id))

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of upvoters
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

    def test_read_comment_upvoters_empty(self):
        # Create a comment
        comment = CommentFactory()

        # Get the upvoters
        response = self.client.get(self.route.format(comment.id))

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of upvoters
        self.assertEqual(len(data), 0)

    def test_read_comment_upvoters_nonexistent(self):
        # Get the upvoters
        response = self.client.get(self.route.format(404))

        # Check status code
        self.assertEqual(response.status_code, 404)
