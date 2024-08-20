# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory

# Managers
from app.managers.comment import CommentBookmarkManager


class TestReadBookmarkedComments(BaseTestCase):
    def test_read_bookmarked_comments(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = CommentBookmarkFactory.create_batch(n, user=user)

        # Read user bookmarks
        bookmarked_comments = CommentBookmarkManager.read_bookmarked_comments_by_user(user)

        # Assert the number of bookmarks
        self.assertEqual(len(bookmarked_comments), n)

        # Get the comments from the bookmarks
        comments = [bookmark.comment for bookmark in bookmarks]

        # Assert the bookmarks are the same
        self.assertEqual(bookmarked_comments, comments)

    def test_read_bookmarked_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Read user bookmarks
        bookmarks_to_read = CommentBookmarkManager.read_bookmarked_comments_by_user(user)

        # Assert the number of bookmarks
        self.assertEqual(len(bookmarks_to_read), 0)

        # Assert that the bookmarks are an empty list
        self.assertEqual(bookmarks_to_read, [])