# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.post_vote_factory import PostVoteFactory


class TestIsUpvote(BaseTestCase):
    def test_is_upvote_true(self):
        # Create a vote
        vote = PostVoteFactory(direction=1)

        # Assert that the post is upvoted
        self.assertTrue(vote.is_upvote())

    def test_is_upvote_false(self):
        # Create a vote
        vote = PostVoteFactory(direction=-1)

        # Assert that the post is not upvoted
        self.assertFalse(vote.is_upvote())
