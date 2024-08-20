# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory

# Errors
from app.errors.errors import BookmarkError

# Factories
from tests.factories.comment_factory import CommentFactory

# Managers
from app.managers.comment import CommentBookmarkManager


class TestDeleteBookmark(BaseTestCase):
    def test_unbookmark_comment(self):
        # Create a bookmarked comment
        bookmark = CommentBookmarkFactory()

        # Get the user
        user = bookmark.user

        # Get the comment
        comment = bookmark.comment

        # Unbookmark the comment
        CommentBookmarkManager.delete(user, comment)

        # Assert that the comment was unbookmarked
        self.assertNotIn(comment, user.comment_bookmarks)

    def test_unbookmark_comment_not_bookmarked(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Attempt to unbookmark the comment again
        with self.assertRaises(BookmarkError):
            CommentBookmarkManager.delete(user, comment)