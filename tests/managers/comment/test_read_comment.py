# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory

# Errors
from app.errors.errors import NotFoundError

# Managers
from app.managers.comment import CommentManager


class TestReadComment(BaseTestCase):
    def test_read_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Read the comment
        comment_to_read = CommentManager.read(comment.id)

        # Assert that the comment is the same
        self.assertEqual(comment, comment_to_read)

    def test_read_comment_not_found(self):
        # Attempt to read a comment that does not exist
        with self.assertRaises(NotFoundError):
            CommentManager.read(0)