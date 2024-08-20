# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.post_bookmark_factory import PostBookmarkFactory

# Models
from app.models.post import PostBookmark


class TestGetByUserAndPost(BaseTestCase):
    def test_get_by_user_and_post(self):
        # Create a post bookmark
        bookmark = PostBookmarkFactory()

        # Get the user the post bookmark
        user = bookmark.user

        # Get the post from the post bookmark
        post = bookmark.post

        # Get the post bookmark by user and post
        bookmark = PostBookmark.get_by_user_and_post(user, post)

        # Assert the post bookmark
        self.assertIsNotNone(bookmark)

    def test_get_by_user_and_post_none(self):
        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Get the post bookmark by user and post    
        bookmark = PostBookmark.get_by_user_and_post(user, post)

        # Assert the post bookmark
        self.assertIsNone(bookmark)

