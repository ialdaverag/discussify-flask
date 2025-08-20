# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_bookmark_factory import PostBookmarkFactory

# Models
from app.models.post import PostBookmark

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetBookmarksByUser(BasePaginationTest):
    def test_get_bookmarks_by_user(self):
        # Number of bookmarks
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = PostBookmarkFactory.create_batch(n, user=user)

        # Set the args
        args = {}

        # Get the bookmarks by user
        bookmarks_by_user = PostBookmark.get_bookmarks_by_user(user, args)

        # Assert that bookmarks_by_user is a Pagination object
        self.assertIsInstance(bookmarks_by_user, Pagination)

        # Get the items
        items = bookmarks_by_user.items

        # Assert the number of bookmarks
        self.assertEqual(len(items), n)

    def test_get_bookmarks_by_user_none(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Get the bookmarks by user
        bookmarks_by_user = PostBookmark.get_bookmarks_by_user(user, args)

        # Assert that bookmarks_by_user is a Pagination object
        self.assertIsInstance(bookmarks_by_user, Pagination)

        # Get the items
        items = bookmarks_by_user.items

        # Assert the number of bookmarks
        self.assertEqual(len(items), 0)