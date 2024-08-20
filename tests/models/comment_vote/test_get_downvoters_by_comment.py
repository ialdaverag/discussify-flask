# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Models
from app.models.comment import CommentVote


class TestGetDownvotersByComment(BaseTestCase):
    def test_get_downvoters_by_comment(self):
        # Number of downvotes
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some votes
        votes = CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Get the downvoters by comment
        downvoters_by_comment = CommentVote.get_downvoters_by_comment(comment)

        # Assert the number of downvoters
        self.assertEqual(len(votes), n)

        # Get the downvoters
        downvoters = [vote.user for vote in votes]

        # Assert that the downvoters are the same
        self.assertEqual(downvoters_by_comment, downvoters)

    def test_get_downvoters_by_comment_none(self):
        # Create a comment
        comment = CommentFactory()

        # Get the downvoters by comment
        downvoters_by_comment = CommentVote.get_downvoters_by_comment(comment)

        # Assert the number of downvoters
        self.assertEqual(len(downvoters_by_comment), 0)

        # Assert that the downvoters list is empty
        self.assertEqual(downvoters_by_comment, [])