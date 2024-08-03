# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.post_vote_factory import PostVoteFactory


class TestIsDownvotedBy(BaseTestCase):
    def test_is_downvoted_by_true(self):
        # Create a vote
        vote = PostVoteFactory(direction=-1)

        # Get the
        user = vote.user

        # Get the post
        post = vote.post

        # Assert that the post is downvoted by the user
        self.assertTrue(post.is_downvoted_by(user))

    def test_is_downvoted_by_false(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Assert that the post is not downvoted by the user
        self.assertFalse(post.is_downvoted_by(user))

    def test_is_downvoted_by_false_upvoted(self):
        # Create a vote
        vote = PostVoteFactory(direction=1)

        # Get the user
        user = vote.user

        # Get the post
        post = vote.post

        # Assert that the post is not downvoted by the user
        self.assertFalse(post.is_downvoted_by(user))
