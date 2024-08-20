# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

from app.managers.comment import CommentVoteManager


class TestReadUpvoters(BaseTestCase):
    def test_read_upvoters(self):
        # Number of upvotes
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some votes
        upvotes = CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Read the comment upvoters
        upvoters = CommentVoteManager.read_upvoters_by_comment(comment)

        # Assert the number of upvotes
        self.assertEqual(len(upvoters), n)

        # Get the users
        users = [upvote.user for upvote in upvotes]

        # Assert that the users are unique
        self.assertEqual(upvoters, users)            


    def test_read_upvoters_empty(self):
        # Create a comment
        comment = CommentFactory()

        # Read the upvoters of the comment
        upvoters = CommentVoteManager.read_upvoters_by_comment(comment)

        # Assert that there are no upvoters
        self.assertEqual(len(upvoters), 0)

        # Assert that the upvoters are an empty list
        self.assertEqual(upvoters, [])