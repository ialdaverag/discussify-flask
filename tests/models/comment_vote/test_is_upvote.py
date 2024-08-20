# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_vote_factory import CommentVoteFactory


class TestIsUpvote(BaseTestCase):
    def test_is_upvote_true(self):
        # Create a vote
        vote = CommentVoteFactory(direction=1)

        # Assert that the comment is upvoted
        self.assertTrue(vote.is_upvote())

    def test_is_upvote_false(self):
        # Create a vote
        vote = CommentVoteFactory(direction=-1)

        # Assert that the comment is not upvoted
        self.assertFalse(vote.is_upvote())