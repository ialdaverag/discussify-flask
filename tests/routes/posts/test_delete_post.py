# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunityModerator


class TestDeletePost(BaseTestCase):
    route = '/post/{}'

    def test_delete_post(self):
        # Create a post
        post = PostFactory()

        # Get the owner of the post
        owner = post.owner

        # Get the access token
        access_token = get_access_token(owner)

        # Delete the post
        response = self.client.delete(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 204)

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
        response = self.client.delete(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 204)

    def test_delete_post_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Delete the post
        response = self.client.delete(
            self.route.format(1),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 404)

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
        response = self.client.delete(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 403)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You cannot delete this post.')