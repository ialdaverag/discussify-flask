# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.post_bookmark_factory import PostBookmarkFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.post import PostBookmark
from app.models.user import Block


class TestBookmarkPost(BaseTestCase):
    route = '/post/{}/bookmark'

    def test_bookmark_post(self):
        # Create a post
        post = PostFactory()

        # Get the user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the post
        response = self.client.post(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 204)

    def test_bookmark_post_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the post
        response = self.client.post(
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

    def test_bookmark_post_owner_blocked_by_user(self):
        # Create a post
        post = PostFactory()

        # Get the user
        user = UserFactory()

        # Get the user
        owner = post.owner

        # Create a block
        Block(blocker=user, blocked=owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the post
        response = self.client.post(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You cannot bookmark this post.')

    def test_bookmark_post_user_blocked_by_owner(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the user
        owner = post.owner

        # Create a block
        Block(blocker=owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the post
        response = self.client.post(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You cannot bookmark this post.')

    def test_bookmark_post_already_bookmarked(self):
        # Create a bookmarked post
        bookmark = PostBookmarkFactory()

        # Get the user
        user = bookmark.user

        # Get the post
        post = bookmark.post

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the post again
        response = self.client.post(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Post already bookmarked.')
