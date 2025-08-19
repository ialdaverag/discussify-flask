# Base
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory
from tests.factories.post_factory import PostFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan


class TestCancelVoteOnPost(TestRoute):
    route = '/post/{}/vote/cancel'

    def test_cancel_vote_on_post(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's community's subscribers
        community = post.community
        CommunitySubscriber(community=community, user=user).save()

        # Create a vote on the post
        PostVoteFactory(user=user, post=post, direction=1)

        # Get the access token
        access_token = get_access_token(user)

        # Upvote the post
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 204)

    def test_cancel_vote_on_post_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Cancel the vote on the post
        response = self.POSTRequest(self.route.format(404), token=access_token)

        # Check status code
        self.assertStatusCode(response, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Post not found.')

    def test_cancel_vote_on_post_being_banned(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's community's banned
        community = post.community
        CommunityBan(community=community, user=user).save()

        # Create a vote on the post
        PostVoteFactory(user=user, post=post, direction=1)

        # Get the access token
        access_token = get_access_token(user)

        # Cancel the vote on the post
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are banned from this community.')

    def test_cancel_vote_on_post_not_being_subscribed(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Create a vote on the post
        PostVoteFactory(user=user, post=post, direction=1)

        # Get the access token
        access_token = get_access_token(user)

        # Cancel the vote on the post
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are not subscribed to this community.')

    def test_cancel_vote_on_post_not_voted(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's community's subscribers
        community = post.community
        CommunitySubscriber(community=community, user=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Cancel the vote on the post
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You have not voted on this post.')