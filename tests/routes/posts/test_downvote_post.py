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
from app.models.user import Block


class TestDownvotePost(TestRoute):
    route = '/post/{}/vote/down'

    def test_downvote_post(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's community's subscribers
        community = post.community
        CommunitySubscriber(community=community, user=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the post
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 204)

    def test_downvote_post_owner_blocked_by_user(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the community
        community = post.community

        # Append the user to the post's community's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Get the post's owner
        owner = post.owner

        # Block the post's owner
        Block(blocker=user, blocked=owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the post
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You cannot vote on this post.')

    def test_downvote_post_userr_blocked_by_owner(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the community
        community = post.community

        # Append the user to the post's community's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Get the post's owner
        owner = post.owner

        # Block the user
        Block(blocker=owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the post
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You cannot vote on this post.')


    def test_downvote_post_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the post
        response = self.POSTRequest(self.route.format(404), token=access_token)

        # Check status code
        self.assertStatusCode(response, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Post not found.')

    def test_downvote_post_being_banned(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's community's subscribers
        community = post.community
        CommunitySubscriber(community=community, user=user).save()

        # Append the user to the post's community's banned
        community = post.community
        CommunityBan(community=community, user=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the post
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are banned from this community.')

    def test_downvote_post_not_subscribed(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the post
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are not subscribed to this community.')

    def test_downvote_post_already_downvoted(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's community's subscribers
        community = post.community
        CommunitySubscriber(community=community, user=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Create a post vote
        PostVoteFactory(
            post=post,
            user=user,
            direction=-1
        )

        # Downvote the post
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Post already downvoted.')