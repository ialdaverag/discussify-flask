# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory

# Managers
from app.managers.comment import CommentBookmarkManager


# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadBookmarksByUser(BaseTestCase):
    def test_read_bookmarks_by_user(self):
        # Number of bookmarks
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        CommentBookmarkFactory.create_batch(n, user=user)

        # Set the args
        args = {}

        # read the bookmarks by user
        bookmarks_by_user = CommentBookmarkManager.read_bookmarked_comments_by_user(user, args)

        # Assert bookmarks_by_user is a Pagination object
        self.assertIsInstance(bookmarks_by_user, Pagination)

        # read the items
        items = bookmarks_by_user.items

        # Assert items is a list
        self.assertIsInstance(items, list)

        # Assert the number of bookmarks
        self.assertEqual(len(items), n)

    def test_read_bookmarks_by_user_none(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # read the bookmarks by user
        bookmarks_by_user = CommentBookmarkManager.read_bookmarked_comments_by_user(user, args)

        # Assert bookmarks_by_user is a Pagination object
        self.assertIsInstance(bookmarks_by_user, Pagination)

        # read the items
        items = bookmarks_by_user.items

        # Assert items is a list
        self.assertIsInstance(items, list)

        # Assert the number of bookmarks
        self.assertEqual(len(items), 0)

