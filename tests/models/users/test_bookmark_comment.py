# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Errors
from app.errors.errors import BookmarkError


class TestBookmarkComment(BaseTestCase):
    def test_bookmark_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Bookmark the comment
        user.bookmark_comment(comment)

        # Assert that the comment was bookmarked
        self.assertIn(comment, user.comment_bookmarks)

    def test_bookmark_comment_already_bookmarked(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Append the comment to the user's bookmarks
        comment.append_bookmarker(user)

        # Attempt to bookmark the comment again
        with self.assertRaises(BookmarkError):
            user.bookmark_comment(comment)
