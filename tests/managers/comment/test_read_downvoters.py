# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

from app.managers.comment import CommentVoteManager


class TestReadDownvoters(BaseTestCase):
    def test_read_downvoters(self):
        # Number of downvotes
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some votes
        downvotes = CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Read the comment downvoters
        downvoters = CommentVoteManager.read_downvoters_by_comment(comment)

        # Assert the number of downvotes
        self.assertEqual(len(downvoters), n)

        # Get the users
        users = [downvote.user for downvote in downvotes]

        # Assert that the users are unique
        self.assertEqual(downvoters, users)            


    def test_read_downvoters_empty(self):
        # Create a comment
        comment = CommentFactory()

        # Read the downvoters of the comment
        downvoters = CommentVoteManager.read_downvoters_by_comment(comment)

        # Assert that there are no downvoters
        self.assertEqual(len(downvoters), 0)

        # Assert that the downvoters are an empty list
        self.assertEqual(downvoters, [])