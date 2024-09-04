# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory

# Models
from app.models.comment import Comment

# Flaks-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetComments(BaseTestCase):
    def test_get_comments(self):
        # Number of comments
        n = 5

        # Create a comment
        CommentFactory.create_batch(n)

        # Set the args
        args = {}

        # get the comment
        comments = Comment.get_all(args)

        # Assert comments is a Pagination object
        self.assertIsInstance(comments, Pagination)

        # Get the items
        comments_items = comments.items

        # Assert the number of comments
        self.assertEqual(len(comments_items), n)


    def test_get_comments_empty(self):
        # Set the args
        args = {}

        # get the comment
        comments = Comment.get_all(args)

        # Assert comments is a Pagination object
        self.assertIsInstance(comments, Pagination)

        # Get the items
        comments_items = comments.items

        # Assert the number of comments
        self.assertEqual(len(comments_items), 0)