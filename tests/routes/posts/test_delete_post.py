# Base
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunityModerator


class TestDeletePost(TestRoute):
    route = '/post/{}'

    def test_delete_post(self):
        # Create a post
        post = PostFactory()

        # Get the owner of the post
        owner = post.owner

        # Get the access token
        access_token = get_access_token(owner)

        # Delete the post
        response = self.DELETERequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 204)

    def test_delete_post_as_moderator(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the community of the post
        community = post.community

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Delete the post
        response = self.DELETERequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 204)

    def test_delete_post_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Delete the post
        response = self.DELETERequest(self.route.format(1), token=access_token)

        # Check status code
        self.assertStatusCode(response, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Post not found.')

    def test_delete_post_not_being_owner(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Delete the post
        response = self.DELETERequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 403)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You cannot delete this post.')