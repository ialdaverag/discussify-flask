# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Models
from app.models.comment import Comment

# Flaks-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetAllByUser(BaseTestCase):
    def test_get_all_by_user(self):
        # Create a user
        user = UserFactory()

        # Number of comments to create
        n = 5

        # Create a comment
        CommentFactory.create_batch(n, owner=user)

        # Set the args
        args = {}

        # Get all comments by the user
        comments_by_user = Comment.get_all_by_user(user, args)

        # Assert the type of comments_by_user
        self.assertIsInstance(comments_by_user, Pagination)

        # Get the items
        items = comments_by_user.items

        # Assert the number of comments
        self.assertEqual(len(items), n)

    def test_get_all_by_user_empty(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Get all comments by the user
        comments_by_user = Comment.get_all_by_user(user, args)

        # Assert the type of comments_by_user
        self.assertIsInstance(comments_by_user, Pagination)

        # Get the items
        items = comments_by_user.items

        # Assert the number of comments
        self.assertEqual(len(items), 0)

