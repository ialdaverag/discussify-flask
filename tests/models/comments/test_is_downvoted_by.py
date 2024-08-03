# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_vote_factory import CommentVoteFactory


class TestIsDownvotedBy(BaseTestCase):
    def test_is_downvoted_by_true(self):
        # Create a vote
        vote = CommentVoteFactory(direction=-1)

        # Get the
        user = vote.user

        # Get the comment
        comment = vote.comment

        # Assert that the post is downvoted by the user
        self.assertTrue(comment.is_downvoted_by(user))

    def test_is_downvoted_by_false(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Assert that the comment is not downvoted by the user
        self.assertFalse(comment.is_downvoted_by(user))

    def test_is_downvoted_by_false_upvoted(self):
        # Create a vote
        vote = CommentVoteFactory(direction=1)

        # Get the user
        user = vote.user

        # Get the comment
        comment = vote.comment

        # Assert that the comment is not downvoted by the user
        self.assertFalse(comment.is_downvoted_by(user))