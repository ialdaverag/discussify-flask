# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Errors
from app.errors.errors import SubscriptionError
from app.errors.errors import BanError
from app.errors.errors import VoteError
from app.errors.errors import BlockError

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan
from app.models.comment import CommentVote
from app.models.user import Block

# Factories
from tests.factories.comment_factory import CommentFactory

# Managers
from app.managers.comment import CommentVoteManager


class TestCreateComment(BaseTestCase):
    def test_vote_positive_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the comment's community
        community = comment.post.community

        # Append the user to the comment's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Upvote the comment
        CommentVoteManager.create(user, comment, 1)

        # Get the comment vote
        vote = CommentVote.get_by_user_and_comment(user, comment)

        # Assert that the comment vote was created
        self.assertIsNotNone(vote)

    def test_vote_positive_comment_voted_negative(self):
        # Create a comment vote
        vote = CommentVoteFactory(direction=-1)

        # Get the comment
        comment = vote.comment

        # Get the user
        user = vote.user

        # Get the comment's community
        community = comment.post.community

        # Append the user to the comment's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Upvote the comment
        CommentVoteManager.create(user, comment, 1)

        # Get the comment vote
        vote = CommentVote.get_by_user_and_comment(user, comment)

        # Assert that the comment vote was created
        self.assertIsNotNone(vote)

    def test_vote_positive_with_owner_blocked(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Subscribe the user to the comment's community
        CommunitySubscriber(community=comment.post.community, user=user).save()

        # Get the comment owner
        owner = comment.owner

        # Block the user
        Block(blocker=user, blocked=owner).save()

        # Attempt to upvote the comment
        with self.assertRaises(BlockError):
            CommentVoteManager.create(user, comment, 1)

    def test_vote_positive_with_user_blocked_by_owner(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Submit the user to the comment's community subscribers
        CommunitySubscriber(community=comment.post.community, user=user).save()

        # Get the comment owner
        owner = comment.owner

        # Block the user
        Block(blocker=owner, blocked=user).save()

        # Attempt to upvote the comment
        with self.assertRaises(BlockError):
            CommentVoteManager.create(user, comment, 1)

    def test_vote_positive_comment_being_banned(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the comment's community
        community = comment.post.community

        # Append the user to the comment's banned users
        CommunityBan(community=community, user=user).save()

        # Attempt to upvote the comment
        with self.assertRaises(BanError):
            CommentVoteManager.create(user, comment, 1)

    def test_vote_positive_comment_not_subscribed(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Attempt to upvote the comment
        with self.assertRaises(SubscriptionError):
            CommentVoteManager.create(user, comment, 1)

    def test_vote_positive_comment_already_upvoted(self):
        # Create a comment vote
        vote = CommentVoteFactory(direction=1)

        # Get the comment
        comment = vote.comment

        # Get the user
        user = vote.user

        # Get the comment's community
        community = comment.post.community

        # Append the user to the comments's community subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Attempt to upvote the comment again
        with self.assertRaises(VoteError):
            CommentVoteManager.create(user, comment, 1)

    def test_vote_negative_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the comment's community
        community = comment.post.community

        # Append the user to the comment's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Downvote the comment
        CommentVoteManager.create(user, comment, -1)

        # Get the comment vote
        vote = CommentVote.get_by_user_and_comment(user, comment)

        # Assert that the comment vote was created
        self.assertIsNotNone(vote)

    def test_vote_negative_comment_voted_positive(self):
        # Create a comment vote
        vote = CommentVoteFactory(direction=1)

        # Get the comment
        comment = vote.comment

        # Get the user
        user = vote.user

        # Get the comment's community
        community = comment.post.community

        # Append the user to the comment's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Downvote the comment
        CommentVoteManager.create(user, comment, -1)

        # Get the comment vote
        vote = CommentVote.get_by_user_and_comment(user, comment)

        # Assert that the comment vote was created
        self.assertIsNotNone(vote)

    def test_vote_negative_comment_being_banned(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the comment's community
        community = comment.post.community

        # Append the user to the comment's banned users
        CommunityBan(community=community, user=user).save()

        # Attempt to downvote the comment
        with self.assertRaises(BanError):
            CommentVoteManager.create(user, comment, -1)

    def test_vote_negative_comment_not_subscribed(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Attempt to downvote the comment
        with self.assertRaises(SubscriptionError):
            CommentVoteManager.create(user, comment, -1)

    def test_vote_negative_comment_already_downvoted(self):
        # Create a comment vote
        vote = CommentVoteFactory(direction=-1)

        # Get the comment
        comment = vote.comment

        # Get the user
        user = vote.user

        # Get the comment's community
        community = comment.post.community

        # Append the user to the comments's community subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Attempt to downvote the comment again
        with self.assertRaises(VoteError):
            CommentVoteManager.create(user, comment, -1)