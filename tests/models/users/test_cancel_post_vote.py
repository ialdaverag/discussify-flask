# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Errors
from app.errors.errors import OwnershipError
from app.errors.errors import BanError
from app.errors.errors import SubscriptionError
from app.errors.errors import VoteError


class TestCancelPostVote(BaseTestCase):
    def test_cancel_post_vote(self):
        # Get the post vote
        vote = PostVoteFactory()

        # Get the user of the vote
        user = vote.user

        # Get the post
        post = vote.post

        # Append the user to the post's community subscribers
        post.community.append_subscriber(user)

        # Cancel the post vote
        user.cancel_post_vote(post)

        # Assert that the post vote was deleted
        self.assertNotIn(vote, user.post_votes)

    def test_cancel_post_vote_being_banned(self):
        # Get the post vote
        vote = PostVoteFactory()

        # Get the user of the vote
        user = vote.user

        # Get the post
        post = vote.post

        # Append the user to the post's community banned users
        post.community.append_banned(user)

        with self.assertRaises(BanError):
            user.cancel_post_vote(post)

    def test_cancel_post_vote_not_subscribed(self):
        # Get the post vote
        vote = PostVoteFactory()

        # Get the user of the vote
        user = vote.user

        # Get the post
        post = vote.post

        # Attempt to cancel the post vote
        with self.assertRaises(SubscriptionError):
            user.cancel_post_vote(post)

    def test_cancel_post_vote_not_voted(self):
        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Append the user to the post's community subscribers
        post.community.append_subscriber(user)

        # Attempt to cancel the post vote
        with self.assertRaises(VoteError):
            user.cancel_post_vote(post)