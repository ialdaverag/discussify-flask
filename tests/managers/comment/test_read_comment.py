# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.user_factory import UserFactory

# Errors
from app.errors.errors import BlockError

# Models
from app.models.user import Block

# Managers
from app.managers.comment import CommentManager


class TestReadComment(BaseTestCase):
    def test_read_comment_anonymous(self):
        # Create a user
        user = None

        # Create a comment
        comment = CommentFactory()

        # Read the comment
        comment_to_read = CommentManager.read(user, comment)

        # Assert that the comment is the same
        self.assertEqual(comment, comment_to_read)

    def test_read_comment_user(self):
        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Read the comment
        comment_to_read = CommentManager.read(user, comment)

        # Assert that the comment is the same
        self.assertEqual(comment, comment_to_read)

    def test_read_comment_user_blocked_by_owner(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the comment
        owner = comment.owner

        # Block the user
        Block(blocker=owner, blocked=user).save()

        # Read the comment
        with self.assertRaises(BlockError):
            CommentManager.read(user, comment)

    def test_read_comment_user_owner_blocked_by_user(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the comment
        owner = comment.owner

        # Block the owner
        Block(blocker=user, blocked=owner).save()

        # Read the comment
        with self.assertRaises(BlockError):
            CommentManager.read(user, comment)