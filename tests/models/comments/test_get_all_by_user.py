# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Models
from app.models.comment import Comment


class TestGetAllByUser(BaseTestCase):
    def test_get_all_by_user(self):
        # Create a user
        user = UserFactory()

        # Number of comments to create
        n = 5

        # Create a comment
        CommentFactory.create_batch(n, owner=user)

        # Get all comments by the user
        comments_by_user = Comment.get_all_by_user(user)

        # Assert the number of comments
        self.assertEqual(len(comments_by_user), n)

    def test_get_all_by_user_empty(self):
        # Create a user
        user = UserFactory()

        # Get all comments by the user
        comments_by_user = Comment.get_all_by_user(user)

        # Assert that comments_by_user is an empty list
        self.assertEqual(comments_by_user, [])

