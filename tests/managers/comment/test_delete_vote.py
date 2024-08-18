# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Errors
from app.errors.errors import SubscriptionError
from app.errors.errors import BanError
from app.errors.errors import VoteError

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan

# Factories
from tests.factories.comment_factory import CommentFactory

# Managers
from app.managers.comment import CommentVoteManager


class TestUpdateComment(BaseTestCase):
    def test_cancel_comment_vote(self):
        # Get the comment vote
        vote = CommentVoteFactory()

        # Get the user of the vote
        user = vote.user

        # Get the comment
        comment = vote.comment

        # Get the comment's community
        community = comment.post.community

        # Append the user to the comment's community subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Cancel the comment vote
        CommentVoteManager.delete(user, comment)

        

        # Assert that the comment vote was deleted
        self.assertNotIn(vote, user.comment_votes)

    def test_cancel_comment_vote_being_banned(self):
        # Get the comment vote
        vote = CommentVoteFactory()

        # Get the user of the vote
        user = vote.user

        # Get the comment
        comment = vote.comment

        # Get the comment's community
        community = comment.post.community

        # Append the user to the comment's community banned users
        CommunityBan(community=community, user=user).save()

        with self.assertRaises(BanError):
            CommentVoteManager.delete(user, comment)

    def test_cancel_comment_vote_not_subscribed(self):
        # Get the comment vote
        vote = CommentVoteFactory()

        # Get the user of the vote
        user = vote.user

        # Get the comment
        comment = vote.comment

        # Attempt to cancel the comment vote
        with self.assertRaises(SubscriptionError):
            CommentVoteManager.delete(user, comment)

    def test_cancel_comment_vote_not_voted(self):
        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Get the comment's community
        community = comment.post.community

        # Append the user to the comment's community subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Attempt to cancel the comment vote
        with self.assertRaises(VoteError):
            CommentVoteManager.delete(user, comment)
