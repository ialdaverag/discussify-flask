# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Errors
from app.errors.errors import BookmarkError

# Models
from app.models.comment import CommentBookmark

# Factories
from tests.factories.comment_factory import CommentFactory

# Managers
from app.managers.comment import CommentBookmarkManager


class TestDeleteBookmark(BaseTestCase):
    def test_unbookmark_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Append the comment to the user's bookmarks
        CommentBookmark(user=user, comment=comment).save()

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