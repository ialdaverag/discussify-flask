# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Errors
from app.errors.errors import BanError
from app.errors.errors import SubscriptionError
from app.errors.errors import VoteError


class TestCancelCommentVote(BaseTestCase):
    def test_cancel_comment_vote(self):
        # Get the comment vote
        vote = CommentVoteFactory()

        # Get the user of the vote
        user = vote.user

        # Get the comment
        comment = vote.comment

        # Append the user to the comment's community subscribers
        comment.post.community.append_subscriber(user)

        # Cancel the comment vote
        user.cancel_comment_vote(comment)

        # Assert that the comment vote was deleted
        self.assertNotIn(vote, user.comment_votes)

    def test_cancel_comment_vote_being_banned(self):
        # Get the comment vote
        vote = CommentVoteFactory()

        # Get the user of the vote
        user = vote.user

        # Get the comment
        comment = vote.comment

        # Append the user to the comment's community banned users
        comment.post.community.append_banned(user)

        with self.assertRaises(BanError):
            user.cancel_comment_vote(comment)

    def test_cancel_comment_vote_not_subscribed(self):
        # Get the comment vote
        vote = CommentVoteFactory()

        # Get the user of the vote
        user = vote.user

        # Get the comment
        comment = vote.comment

        # Attempt to cancel the comment vote
        with self.assertRaises(SubscriptionError):
            user.cancel_comment_vote(comment)

    def test_cancel_comment_vote_not_voted(self):
        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Append the user to the comment's community subscribers
        comment.post.community.append_subscriber(user)

        # Attempt to cancel the comment vote
        with self.assertRaises(VoteError):
            user.cancel_comment_vote(comment)