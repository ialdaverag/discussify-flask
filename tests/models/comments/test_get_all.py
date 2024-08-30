# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory

# Models
from app.models.comment import Comment


class TestGetAll(BaseTestCase):
    def test_get_all(self):
        # Number of comments to create
        n = 5

        # Create a comment
        CommentFactory.create_batch(n)

        # Get all comments
        comments = Comment.get_all()

        # Assert the number of comments
        self.assertEqual(len(comments), n)

    def test_get_all_empty(self):
        # Get all comments
        comments = Comment.get_all()

        # Assert that comments is an empty list
        self.assertEqual(comments, [])