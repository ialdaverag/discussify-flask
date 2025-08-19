# Base
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.post_bookmark_factory import PostBookmarkFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.post import PostBookmark
from app.models.user import Block


class TestBookmarkPost(TestRoute):
    route = '/post/{}/bookmark'

    def test_bookmark_post(self):
        # Create a post
        post = PostFactory()

        # Get the user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the post
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 204)

    def test_bookmark_post_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the post
        response = self.POSTRequest(self.route.format(1), token=access_token)

        # Check status code
        self.assertStatusCode(response, 404)

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
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

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
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

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
        response = self.POSTRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Post already bookmarked.')
