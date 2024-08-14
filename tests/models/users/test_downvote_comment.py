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

# Models
from app.models.comment import CommentVote
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan


class TestDownvoteComment(BaseTestCase):
    def test_downvote_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the comment's subscribers
        community = comment.post.community
        CommunitySubscriber(community=community, user=user).save()

        # Downvote the comment
        user.downvote_comment(comment)

        # Get the comment vote
        vote = CommentVote.get_by_user_and_comment(user, comment)

        # Assert that the comment vote was created
        self.assertIsNotNone(vote)

    def test_downvote_comment_being_banned(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the comment's banned users
        community = comment.post.community
        CommunityBan(community=community, user=user).save()

        # Attempt to downvote the comment
        with self.assertRaises(BanError):
            user.downvote_comment(comment)

    def test_downvote_comment_not_subscribed(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Attempt to downvote the comment
        with self.assertRaises(SubscriptionError):
            user.downvote_comment(comment)

    def test_downvote_comment_already_downvoted(self):
        # Create a comment vote
        vote = CommentVoteFactory(direction=-1)

        # Get the comment
        comment = vote.comment

        # Get the user
        user = vote.user

        # Append the user to the comments's community subscribers
        community = comment.post.community
        CommunitySubscriber(community=community, user=user).save()

        # Attempt to downvote the comment again
        with self.assertRaises(VoteError):
            user.downvote_comment(comment)