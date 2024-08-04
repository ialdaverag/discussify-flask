# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.post_vote_factory import PostVoteFactory


class TestIsDownvote(BaseTestCase):
    def test_is_downvote_true(self):
        # Create a vote
        vote = PostVoteFactory(direction=-1)

        # Assert that the post is downvoted
        self.assertTrue(vote.is_downvote())

    def test_is_downvote_false(self):
        # Create a vote
        vote = PostVoteFactory(direction=1)

        # Assert that the post is not downvoted
        self.assertFalse(vote.is_downvote())
