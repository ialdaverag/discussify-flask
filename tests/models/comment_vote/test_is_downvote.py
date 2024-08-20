# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_vote_factory import CommentVoteFactory


class TestIsDownvote(BaseTestCase):
    def test_is_downvote_true(self):
        # Create a vote
        vote = CommentVoteFactory(direction=-1)

        # Assert that the comment is downvoted
        self.assertTrue(vote.is_downvote())

    def test_is_downvote_false(self):
        # Create a vote
        vote = CommentVoteFactory(direction=1)

        # Assert that the comment is not downvoted
        self.assertFalse(vote.is_downvote())
