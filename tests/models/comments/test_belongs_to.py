# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory


class TestBelongsTo(BaseTestCase):
    def test_belongs_to_true(self):
        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory(owner=user)

        # Assert that the user belongs to the comment
        self.assertTrue(comment.belongs_to(user))

    def test_belongs_to_false(self):
        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Assert that the user does not belong to the comment
        self.assertFalse(comment.belongs_to(user))
