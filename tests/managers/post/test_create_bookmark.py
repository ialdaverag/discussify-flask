# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_bookmark_factory import PostBookmarkFactory

# Models
from app.models.post import PostBookmark

# Errors
from app.errors.errors import BookmarkError

# Managers
from app.managers.post import PostBookmarkManager

# Factories
from tests.factories.post_factory import PostFactory


class TestCreateBookmark(BaseTestCase):
    def test_bookmark_post(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Bookmark the post
        PostBookmarkManager.create(user, post)

        # Retrieve the bookmark
        bookmark = PostBookmark.get_by_user_and_post(user, post)

        # Assert that the post was bookmarked
        self.assertIsNotNone(bookmark)

    def test_bookmark_post_already_bookmarked(self):
        # Create a bookmarked post
        bookmark = PostBookmarkFactory()

        # Get the user
        user = bookmark.user

        # Get the post
        post = bookmark.post

        # Attempt to bookmark the post again
        with self.assertRaises(BookmarkError):
            PostBookmarkManager.create(user, post)