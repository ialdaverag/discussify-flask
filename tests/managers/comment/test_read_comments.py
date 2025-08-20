# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.comment_factory import CommentFactory

# Managers
from app.managers.comment import CommentManager

# Flaks-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadComments(BasePaginationTest):
    def test_read_comments(self):
        # Number of comments
        n = 5

        # Create a comment
        CommentFactory.create_batch(n)

        # Set the args
        args = {}

        # Read the comment
        comments = CommentManager.read_all(args)

        # Assert comments is a Pagination object
        self.assertIsInstance(comments, Pagination)

        # Get the items
        comments_items = comments.items

        # Assert the number of comments
        self.assertEqual(len(comments_items), n)


    def test_read_comments_empty(self):
        # Set the args
        args = {}

        # Read the comment
        comments = CommentManager.read_all(args)

        # Assert comments is a Pagination object
        self.assertIsInstance(comments, Pagination)

        # Get the items
        comments_items = comments.items

        # Assert the number of comments
        self.assertEqual(len(comments_items), 0)