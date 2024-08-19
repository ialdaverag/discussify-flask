# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Models
from app.models.comment import CommentBookmark

# Managers
from app.managers.comment import CommentBookmarkManager


class TestReadBookmarkedComments(BaseTestCase):
    def test_read_bookmarked_comments(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user bookmark the comments
        for comment in comments:
            CommentBookmark(user=user, comment=comment).save()

        # Read user bookmarks
        bookmarks_to_read = CommentBookmarkManager.read_bookmarked_comments_by_user(user)

        # Assert the number of bookmarks
        self.assertEqual(len(bookmarks_to_read), n)

        # Assert the bookmarks are the same
        self.assertEqual(comments, bookmarks_to_read)

    def test_read_bookmarked_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Read user bookmarks
        bookmarks_to_read = CommentBookmarkManager.read_bookmarked_comments_by_user(user)

        # Assert the number of bookmarks
        self.assertEqual(len(bookmarks_to_read), 0)

        # Assert that the bookmarks are an empty list
        self.assertEqual(bookmarks_to_read, [])