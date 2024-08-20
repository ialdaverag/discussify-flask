# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory

# Models
from app.models.comment import CommentBookmark


class TestGetBookmarksByUser(BaseTestCase):
    def test_get_bookmarks_by_user(self):
        # Number of bookmarks
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = CommentBookmarkFactory.create_batch(n, user=user)

        # Get the bookmarks by user
        bookmarks_by_user = CommentBookmark.get_bookmarks_by_user(user)

        # Assert the number of bookmarks
        self.assertEqual(len(bookmarks), n)

        # Get the bookmarks
        comments = [bookmark.comment for bookmark in bookmarks]

        # Assert that the bookmarks are the same
        self.assertEqual(comments, bookmarks_by_user)

    def test_get_bookmarks_by_user_none(self):
        # Create a user
        user = UserFactory()

        # Get the bookmarks by user
        bookmarks_by_user = CommentBookmark.get_bookmarks_by_user(user)

        # Assert the number of bookmarks
        self.assertEqual(len(bookmarks_by_user), 0)

        # Assert that the bookmarks by user is an empty list
        self.assertEqual(bookmarks_by_user, [])
