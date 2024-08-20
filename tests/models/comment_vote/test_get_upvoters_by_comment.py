# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Models
from app.models.comment import CommentVote


class TestGetUpvotersByComment(BaseTestCase):
    def test_get_upvoters_by_comment(self):
        # Number of upvotes
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some votes
        votes = CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Get the upvoters by comment
        upvoters_by_comment = CommentVote.get_upvoters_by_comment(comment)

        # Assert the number of upvoters
        self.assertEqual(len(votes), n)

        # Get the upvoters
        upvoters = [vote.user for vote in votes]

        # Assert that the upvoters are the same
        self.assertEqual(upvoters_by_comment, upvoters)

    def test_get_upvoters_by_comment_none(self):
        # Create a comment
        comment = CommentFactory()

        # Get the upvoters by comment
        upvoters_by_comment = CommentVote.get_upvoters_by_comment(comment)

        # Assert the number of upvoters
        self.assertEqual(len(upvoters_by_comment), 0)

        # Assert that the upvoters list is empty
        self.assertEqual(upvoters_by_comment, [])


