# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Errors
from app.errors.errors import BanError
from app.errors.errors import SubscriptionError
from app.errors.errors import VoteError

# Models
from app.models.post import PostVote


class TestUpvotePost(BaseTestCase):
    def test_upvote_post(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's subscribers
        post.community.append_subscriber(user)

        # Upvote the post
        user.upvote_post(post)

        # Get the post vote
        vote = PostVote.get_by_user_and_post(user, post)

        # Assert that the post vote was created
        self.assertIsNotNone(vote)

    def test_upvote_post_being_banned(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's banned users
        post.community.append_banned(user)

        # Attempt to upvote the post
        with self.assertRaises(BanError):
            user.upvote_post(post)

    def test_upvote_post_not_subscribed(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Attempt to upvote the post
        with self.assertRaises(SubscriptionError):
            user.upvote_post(post)

    def test_upvote_post_already_upvoted(self):
        # Create a post vote
        vote = PostVoteFactory(direction=1)

        # Create a post
        post = vote.post

        # Create a user
        user = vote.user

        # Append the user to the post's subscribers
        post.community.append_subscriber(user)

        # Attempt to upvote the post again
        with self.assertRaises(VoteError):
            user.upvote_post(post)