# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.post_bookmark_factory import PostBookmarkFactory

# Errors
from app.errors.errors import BookmarkError

# Managers
from app.managers.post import PostBookmarkManager


class TestDeleteBookmark(BaseTestCase):
    def test_unbookmark_post(self):
        # Create a bookmarked post
        bookmark = PostBookmarkFactory()

        # Get the user
        user = bookmark.user

        # Get the post
        post = bookmark.post

        # Unbookmark the post
        PostBookmarkManager.delete(user, post)

        # Assert that the post was unbookmarked
        self.assertNotIn(post, user.bookmarks)

    def test_unbookmark_post_not_bookmarked(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Attempt to unbookmark the post again
        with self.assertRaises(BookmarkError):
            PostBookmarkManager.delete(user, post)