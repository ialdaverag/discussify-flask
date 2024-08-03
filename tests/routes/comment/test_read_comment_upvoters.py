# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory
from tests.factories.comment_factory import CommentFactory

# Utils
from tests.utils.tokens import get_access_token


class TestReadCommentUpvoters(BaseTestCase):
    route = '/comment/{}/upvoters'

    def test_read_comment_upvoters(self):
        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        CommentVoteFactory.create_batch(5, comment=comment, direction=1)

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of upvoters
        self.assertEqual(len(data), 5)

    def test_read_comment_upvoters_empty(self):
        # Create a comment
        comment = CommentFactory()

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of upvoters
        self.assertEqual(len(data), 0)

    def test_read_comment_upvoters_nonexistent(self):
        # Get the upvoters
        response = self.client.get(
            self.route.format(404),
        )

        # Check status code
        self.assertEqual(response.status_code, 404)
