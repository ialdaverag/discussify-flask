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
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan

# Managers
from app.managers.post import PostVoteManager


class TestCreateVote(BaseTestCase):
    def test_vote_positive_post(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the post's community
        community = post.community

        # Append the user to the post's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Upvote the post
        PostVoteManager.create(user, post, 1)

        # Get the post vote
        vote = PostVote.get_by_user_and_post(user, post)

        # Assert that the post vote was created
        self.assertIsNotNone(vote)

    def test_vote_positive_post_voted_negative(self):
        # Create a post vote
        vote = PostVoteFactory(direction=-1)

        # Get the post
        post = vote.post

        # Get the user
        user = vote.user

        # Get the post's community
        community = post.community

        # Append the user to the post's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Upvote the post
        PostVoteManager.create(user, post, 1)

        # Get the post vote
        vote = PostVote.get_by_user_and_post(user, post)

        # Assert that the post vote was created
        self.assertIsNotNone

    def test_vote_positive_post_being_banned(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the post's community
        community = post.community

        # Append the user to the post's banned users
        CommunityBan(community=community, user=user).save()

        # Attempt to upvote the post
        with self.assertRaises(BanError):
            PostVoteManager.create(user, post, 1)

    def test_vote_positive_post_not_subscribed(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Attempt to upvote the post
        with self.assertRaises(SubscriptionError):
            PostVoteManager.create(user, post, 1)

    def test_vote_positive_post_already_upvoted(self):
        # Create a post vote
        vote = PostVoteFactory(direction=1)

        # Create a post
        post = vote.post

        # Create a user
        user = vote.user

        # Get the post's community
        community = post.community

        # Append the user to the post's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Attempt to upvote the post again
        with self.assertRaises(VoteError):
            PostVoteManager.create(user, post, 1)

    def test_vote_negative_post(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the post's community
        community = post.community

        # Append the user to the post's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Downvote the post
        PostVoteManager.create(user, post, -1)

        # Get the post vote
        vote = PostVote.get_by_user_and_post(user, post)

        # Assert that the post vote was created
        self.assertIsNotNone(vote)

    def test_vote_negative_post_voted_positive(self):
        # Create a post vote
        vote = PostVoteFactory(direction=1)

        # Get the post
        post = vote.post

        # Get the user
        user = vote.user

        # Get the post's community
        community = post.community

        # Append the user to the post's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Downvote the post
        PostVoteManager.create(user, post, -1)

        # Get the post vote
        vote = PostVote.get_by_user_and_post(user, post)

        # Assert that the post vote was created
        self.assertIsNotNone(vote)

    def test_vote_negative_post_being_banned(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the post's community
        community = post.community

        # Append the user to the post's banned users
        CommunityBan(community=community, user=user).save()

        # Attempt to downvote the post
        with self.assertRaises(BanError):
            PostVoteManager.create(user, post, -1)

    def test_vote_negative_post_not_subscribed(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Attempt to downvote the post
        with self.assertRaises(SubscriptionError):
            PostVoteManager.create(user, post, -1)

    def test_vote_negative_post_already_downvoted(self):
        # Create a post vote
        vote = PostVoteFactory(direction=-1)

        # Create a post
        post = vote.post

        # Create a user
        user = vote.user

        # Get the post's community
        community = post.community

        # Append the user to the post's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Attempt to upvote the post again
        with self.assertRaises(VoteError):
            PostVoteManager.create(user, post, -1)
