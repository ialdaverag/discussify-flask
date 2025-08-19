# Base
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.post_bookmark_factory import PostBookmarkFactory

# Utils
from tests.utils.tokens import get_access_token


class TestUnbookmarkPost(TestRoute):
    route = '/post/{}/unbookmark'

    def test_unbookmark_post(self):
        # Create a bookmarked post
        bookmark = PostBookmarkFactory()

        # Get the user
        user = bookmark.user

        # Get the post
        post = bookmark.post

        # Get the access token
        access_token = get_access_token(user)

        # Unbookmark the post
        response = self.POSTRequest(
            self.route.format(post.id),
            token=access_token
        )

        # Check status code
        self.assertStatusCode(response, 204)

    def test_unbookmark_post_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Unbookmark the post
        response = self.POSTRequest(
            self.route.format(404),
            token=access_token
        )

        # Check status code
        self.assertStatusCode(response, 404)

        # Assert the message
        self.assertMessage(response, 'Post not found.')

    def test_unbookmark_post_not_bookmarked(self):
        # Create a post
        post = PostFactory()

        # Get the user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Unbookmark the post
        response = self.POSTRequest(
            self.route.format(post.id),
            token=access_token
        )

        # Check status code
        self.assertStatusCode(response, 400)

        # Assert the message
        self.assertMessage(response, 'Post not bookmarked.')