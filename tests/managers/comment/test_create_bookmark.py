# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Errors
from app.errors.errors import BookmarkError
from app.errors.errors import BlockError

# Models
from app.models.comment import CommentBookmark
from app.models.user import Block

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory

# Managers
from app.managers.comment import CommentBookmarkManager


class TestCreateBookmark(BaseTestCase):
    def test_bookmark_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Bookmark the comment
        CommentBookmarkManager.create(user, comment)

        # Retrieve the bookmark
        bookmark = CommentBookmark.get_by_user_and_comment(user, comment)

        # Assert that the comment was bookmarked
        self.assertIsNotNone(bookmark)

    def test_bookmark_comment_with_owner_blocked(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the comment owner
        owner = comment.owner

        # Block the user
        Block(blocker=user, blocked=owner).save()

        # Attempt to bookmark the comment
        with self.assertRaises(BlockError):
            CommentBookmarkManager.create(user, comment)

    def test_bookmark_comment_with_user_blocked_by_owner(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the comment owner
        owner = comment.owner

        # Block the user
        Block(blocker=owner, blocked=user).save()

        # Attempt to bookmark the comment
        with self.assertRaises(BlockError):
            CommentBookmarkManager.create(user, comment)

    def test_bookmark_comment_already_bookmarked(self):
        # Create a bookmarked comment
        bookmark = CommentBookmarkFactory()

        # Get the user
        user = bookmark.user

        # Get the comment
        comment = bookmark.comment

        # Attempt to bookmark the comment again
        with self.assertRaises(BookmarkError):
            CommentBookmarkManager.create(user, comment)