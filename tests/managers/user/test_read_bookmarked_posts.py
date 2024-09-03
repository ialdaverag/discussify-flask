# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_bookmark_factory import PostBookmarkFactory

# Managers
from app.managers.post import PostBookmarkManager

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadBookmarksByUser(BaseTestCase):
    def test_read_bookmarks_by_user(self):
        # Number of bookmarks
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        PostBookmarkFactory.create_batch(n, user=user)

        # Set the args
        args = {}

        # read the bookmarks by user
        bookmarks_by_user = PostBookmarkManager.read_bookmarked_posts_by_user(user, args)

        # Assert that bookmarks_by_user is a Pagination object
        self.assertIsInstance(bookmarks_by_user, Pagination)

        # read the items
        items = bookmarks_by_user.items

        # Assert the number of bookmarks
        self.assertEqual(len(items), n)

    def test_read_bookmarks_by_user_none(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # read the bookmarks by user
        bookmarks_by_user = PostBookmarkManager.read_bookmarked_posts_by_user(user, args)

        # Assert that bookmarks_by_user is a Pagination object
        self.assertIsInstance(bookmarks_by_user, Pagination)

        # read the items
        items = bookmarks_by_user.items

        # Assert the number of bookmarks
        self.assertEqual(len(items), 0)